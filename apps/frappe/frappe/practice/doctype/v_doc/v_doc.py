import requests

import frappe
from frappe.model.document import Document


class VDoc(Document):

    @staticmethod
    def get_list(
        filters=None,
        fields=None,
        order_by=None,
        limit_start=0,
        limit_page_length=20,
    ):
        response = requests.get(
            "https://jsonplaceholder.typicode.com/posts",
            timeout=10,
        )
        response.raise_for_status()

        posts = response.json()

        posts = posts[
            limit_start : limit_start + limit_page_length
        ]

        return [
            {
                "name": str(post["id"]),
                "user_id": post["userId"],
                "title": post["title"],
                "body": post["body"],
            }
            for post in posts
        ]

    def load_from_db(self):
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/posts/{self.name}",
            timeout=10,
        )
        response.raise_for_status()

        post = response.json()

        self.user_id = post["userId"]
        self.title = post["title"]
        self.body = post["body"]

        return self