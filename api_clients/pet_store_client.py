import base64
import json
import mimetypes
from pathlib import Path
from playwright.sync_api import APIRequestContext, sync_playwright
from helpers.pw_api_helpers import extract_base_url

class BasicAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_headers(self):
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}",
        }


class PetStoreClient:
    def __init__(self, request_context: APIRequestContext = None):
        self.base_url = extract_base_url("PETSTOREAPI").strip('"').strip("'")
        self.pet_endpoint = f"{self.base_url}/v2/pet"
        self.store_endpoint = f"{self.base_url}/v2/store"
        self._external_request_context = request_context is not None

        if request_context:
            self.api_context = request_context
            self._playwright = None
        else:
            self._playwright = sync_playwright().start()
            self.api_context = self._playwright.request.new_context(base_url=self.base_url)

    def get_pets_by_status(self, status):
        """Sends a GET request to retrieve pets by status."""
        return self.api_context.get("/v2/pet/findByStatus", params={"status": status})

    def get_pet_by_id(self, pet_id):
        """Sends a GET request to retrieve a specific pet by ID."""
        return self.api_context.get(f"/v2/pet/{pet_id}")

    def create_pet(self, payload):
        """Sends a POST request to create a new pet."""
        return self.api_context.post("/v2/pet", json=payload)

    def update_pet(self, payload):
        """Sends a PUT request to update an existing pet."""
        return self.api_context.put("/v2/pet", json=payload)

    def delete_pet(self, pet_id):
        """Sends a DELETE request to remove a pet."""
        return self.api_context.delete(f"/v2/pet/{pet_id}")

    def upload_pet_image(self, pet_id, image_path):
        """Sends a POST request to upload an image for a specific pet."""
        image_bytes = Path(image_path).read_bytes()
        content_type, _ = mimetypes.guess_type(image_path)
        multipart_payload = {
            "file": {
                "name": Path(image_path).name,
                "buffer": image_bytes,
                "mimeType": content_type or "image/jpeg",
            }
        }

        return self.api_context.post(
            f"/v2/pet/{pet_id}/uploadImage",
            multipart=multipart_payload,
        )

    def get_pet_inventory_by_status(self):
        """Sends a GET request to retrieve pet inventory by status."""
        return self.api_context.get("/v2/store/inventory")

    def create_order(self, payload):
        """Sends a POST request to create a new order."""
        return self.api_context.post("/v2/store/order", json=payload)

    def get_order_by_id(self, order_id):
        """Sends a GET request to retrieve a specific order by ID."""
        return self.api_context.get(f"/v2/store/order/{order_id}")

    def delete_order(self, order_id):
        """Sends a DELETE request to remove an order."""
        return self.api_context.delete(f"/v2/store/order/{order_id}")

    def close(self):
        if self.api_context:
            self.api_context.dispose()
        if self._playwright:
            self._playwright.stop()
    