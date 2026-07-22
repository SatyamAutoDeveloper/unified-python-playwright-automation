import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, Optional

import ollama

from helpers.pw_location_chain import LocationChain as LC

logger = logging.getLogger(__name__)

HEALED_LOCATORS_FILE = Path(__file__).resolve().parent / "healed_locators.json"
HEALER_MODEL = os.getenv("HEALER_MODEL", "qwen2.5-coder:7b")
HEALER_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
HEALER_MAX_NEW_TOKENS = int(os.getenv("HEALER_MAX_NEW_TOKENS", "256"))


def _load_healed_locators() -> Dict[str, str]:
    if not HEALED_LOCATORS_FILE.exists():
        return {}
    try:
        return json.loads(HEALED_LOCATORS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_healed_locators(data: Dict[str, str]) -> None:
    HEALED_LOCATORS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _normalize_locator_key(locator_def: Any) -> str:
    chain = getattr(locator_def, "chain", None)
    if not isinstance(chain, list) or not chain:
        return repr(locator_def)

    first_method_name, args, kwargs = chain[0]
    if first_method_name == "locator" and args and isinstance(args[0], str):
        return args[0]

    parts = []
    for method_name, args, kwargs in chain:
        arg_strings = [repr(arg) for arg in args]
        kw_strings = [f"{key}={repr(value)}" for key, value in kwargs.items()]
        parts.append(f"{method_name}({', '.join(arg_strings + kw_strings)})")
    return " > ".join(parts)


def _sanitize_locators(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:[a-zA-Z0-9_-]+)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = re.sub(r"^`+|`+$", "", cleaned)
    return cleaned


def _is_locator_valid(locator: Any) -> bool:
    try:
        return locator.count() > 0
    except Exception:
        return False


def _looks_like_locator(value: str) -> bool:
    candidate = value.strip().strip("`'\".,;:")
    if not candidate:
        return False
    if any(char.isspace() for char in candidate):
        return False
    if candidate.startswith(("page.locator(", "locator(", ".locator(")):
        return True
    if candidate.startswith(("//", ".", "#")):
        return True
    if re.match(r"^(text|role|placeholder|label|alt)=", candidate):
        return True
    if candidate.startswith(("input", "button", "a", "div", "form", "select", "textarea", "span", "label")):
        return "[" in candidate or candidate in {"input", "button", "a", "div", "form", "select", "textarea", "span", "label"}
    return "[" in candidate or "]" in candidate


def _extract_content_from_response(response: Any) -> str:
    if isinstance(response, dict):
        if "message" in response:
            message = response.get("message")
            if isinstance(message, dict):
                content = message.get("content")
            else:
                content = getattr(message, "content", None)
            if isinstance(content, str):
                return content
        if "response" in response:
            response_text = response.get("response")
            if isinstance(response_text, str):
                return response_text
        return str(response)

    if hasattr(response, "message"):
        message = getattr(response, "message")
        if isinstance(message, dict):
            content = message.get("content")
        else:
            content = getattr(message, "content", None)
        if isinstance(content, str):
            return content

    if hasattr(response, "response"):
        response_text = getattr(response, "response")
        if isinstance(response_text, str):
            return response_text

    return str(response)


def _extract_locator_from_response(content: str) -> Optional[str]:
    candidate = _sanitize_locators(content)
    if not candidate:
        return None

    for pattern in (
        r"page\.locator\(\s*[\"']([^\"']+)[\"']\s*\)",
        r"locator\(\s*[\"']([^\"']+)[\"']\s*\)",
    ):
        match = re.search(pattern, candidate, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    for block in re.findall(r"```(?:[a-zA-Z0-9_-]+)?\s*(.*?)```", candidate, re.DOTALL | re.IGNORECASE):
        for line in block.splitlines():
            line = line.strip().strip("`'\".,;:")
            if _looks_like_locator(line):
                return line

    for match in re.finditer(r"`([^`]+)`", candidate):
        value = match.group(1).strip().strip("`'\".,;:")
        if _looks_like_locator(value):
            return value

    for match in re.finditer(r"([a-zA-Z0-9_.:/#\-]+\[[^\]]+\])", candidate):
        value = match.group(1).strip().strip("`'\".,;:")
        if _looks_like_locator(value):
            return value

    for line in candidate.splitlines():
        line = line.strip().strip("`'\".,;:")
        if _looks_like_locator(line):
            return line

    for match in re.finditer(r"[\"']([#.\/\[\]A-Za-z0-9:_=-]{2,})[\"']", candidate):
        value = match.group(1).strip()
        if _looks_like_locator(value):
            return value

    return None


def _infer_locator_from_page(page: Any, locator_key: str) -> Optional[str]:
    page_html = page.content() if hasattr(page, "content") else str(page)
    normalized_key = locator_key.lower()

    if any(token in normalized_key for token in ("uame", "user", "username", "email")):
        for attr_name in re.findall(r'name=[\"\']([^\"\']+)[\"\']', page_html, re.IGNORECASE):
            lower_name = attr_name.lower()
            if any(token in lower_name for token in ("user", "username", "email")):
                return f"input[name='{attr_name}']"
        if re.search(r"<input[^>]+type=['\"]email['\"][^>]*>", page_html, re.IGNORECASE):
            return "input[type='email']"

    if any(token in normalized_key for token in ("pass", "password")):
        for attr_name in re.findall(r'name=[\"\']([^\"\']+)[\"\']', page_html, re.IGNORECASE):
            if "password" in attr_name.lower():
                return f"input[name='{attr_name}']"

    if "login" in normalized_key and re.search(r"<button[^>]+type=['\"]submit['\"][^>]*>", page_html, re.IGNORECASE):
        return "button[type='submit']"

    return None


def _build_ollama_client() -> Any:
    try:
        return ollama.Client(host=HEALER_HOST)
    except Exception as exc:
        raise RuntimeError(f"Unable to initialize Ollama client: {exc}") from exc


def _local_llm_heal_locator(page: Any, locator_key: str) -> str:
    logger.info("Starting locator healing for: %s", locator_key)
    page_html = page.content() if hasattr(page, "content") else str(page)
    prompt = (
        "You are a Playwright locator repair assistant. "
        "Given a broken locator and the current page HTML, return a single replacement locator string "
        "that should work with Playwright's page.locator(...) or locator(...) methods. "
        "Return only the locator string, with no explanation.\n\n"
        f"Broken locator: {locator_key}\n\n"
        "Page HTML:\n"
        f"{page_html[:15000]}"
    )

    try:
        client = _build_ollama_client()
        logger.info("Requesting locator suggestion from Ollama using model: %s", HEALER_MODEL)
        response = client.chat(
            model=HEALER_MODEL,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            options={"num_predict": HEALER_MAX_NEW_TOKENS},
        )
        content = _extract_content_from_response(response)
    except TypeError:
        response = client.generate(
            model=HEALER_MODEL,
            prompt=prompt,
            stream=False,
            options={"num_predict": HEALER_MAX_NEW_TOKENS},
        )
        content = _extract_content_from_response(response)
    except Exception as exc:
        logger.error("Ollama locator generation failed: %s", exc, exc_info=True)
        raise RuntimeError(f"Ollama locator generation failed: {exc}") from exc

    logger.info("Ollama output: %s", content)
    new_locator = _extract_locator_from_response(content)
    if not new_locator:
        heuristic_locator = _infer_locator_from_page(page, locator_key)
        if heuristic_locator:
            logger.info("Heuristic locator inferred from page HTML: %s", heuristic_locator)
            return heuristic_locator
        raise RuntimeError(f"Ollama did not return a usable locator. Raw output: {content}")
    logger.info("Healed locator: %s", new_locator)
    return new_locator


def _build_locator_definition(locator_string: str) -> Any:
    return LC.locator(locator_string)


def _build_fallback_locator_definition(locator_key: str) -> Optional[Any]:
    if not locator_key.startswith("get_by_text("):
        return None

    match = re.search(r"get_by_text\((.+)\)", locator_key)
    if not match:
        return None

    raw_value = match.group(1).strip()
    if len(raw_value) >= 2 and raw_value[0] == raw_value[-1] and raw_value[0] in {"'", '"'}:
        raw_value = raw_value[1:-1]

    if not raw_value:
        return None

    return LC.locator(f"text={raw_value}")


class AutoHealer:
    @staticmethod
    def resolve_or_heal(page: Any, locator_def: Any) -> Any:
        locator_key = _normalize_locator_key(locator_def)
        original_locator = None
        for attempt in range(3):
            try:
                original_locator = locator_def.resolve(page)
                if _is_locator_valid(original_locator):
                    logger.debug(f"Locator resolved successfully on attempt {attempt + 1}: {locator_key}")
                    return original_locator
            except Exception as e:
                logger.debug(f"Attempt {attempt + 1} failed to resolve locator {locator_key}: {e}")
            if attempt < 2:
                time.sleep(0.5)

        healed_locators = _load_healed_locators()
        healed_locator = healed_locators.get(locator_key)
        logger.info(f"Attempting to heal locator for key: {locator_key}")
        if healed_locator:
            try:
                healed_definition = _build_locator_definition(healed_locator)
                healed_result = healed_definition.resolve(page)
                logger.info(f"Using healed locator from cache: {healed_locator}")
                if _is_locator_valid(healed_result):
                    return healed_result
                else:
                    logger.warning(f"Cached healed locator is no longer valid: {healed_locator}")
            except Exception as e:
                logger.warning(f"Cached healed locator failed: {healed_locator}. Error: {e}")

        try:
            new_locator = _local_llm_heal_locator(page, locator_key)
            healed_locators[locator_key] = new_locator
            _save_healed_locators(healed_locators)
            healed_definition = _build_locator_definition(new_locator)
            logger.info(f"Using locally healed locator: {new_locator}")
            healed_result = healed_definition.resolve(page)
            if _is_locator_valid(healed_result):
                return healed_result
        except Exception:
            logger.info(f"Local locator healing unavailable for key: {locator_key}")

        fallback_definition = _build_fallback_locator_definition(locator_key)
        if fallback_definition:
            try:
                fallback_result = fallback_definition.resolve(page)
                if _is_locator_valid(fallback_result):
                    logger.info(f"Using fallback locator for key: {locator_key}")
                    return fallback_result
            except Exception as e:
                logger.debug(f"Fallback locator failed for key: {locator_key}: {e}")

        if original_locator is not None:
            try:
                logger.warning(f"All healing attempts failed. Returning original unresolved locator for: {locator_key}")
                return original_locator
            except Exception as e:
                logger.error(f"Original locator also failed to resolve: {e}")

        logger.error(f"Failed to heal locator for key: {locator_key}. No fallback available.")
        return locator_def.resolve(page)
