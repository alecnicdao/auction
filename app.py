from flask import Flask, render_template

app = Flask(__name__)

categories = {
    "collectables": {
        "items": {
            "card": {
                "title": "Honus Wagner - 2009 Topps (PSA GEM MT 10)",
                "img": "img/card.jpg",
                "description": "2009 TOPPS T-206 HONUS WAGNER PSA GEM MT 10. Shipped with USPS First Class.",
                "price": "$259,000.00",
            },
        },
        "title": "Collectibles & Art",
        "subtitle": "Discover coins, stamps, comics, and more.",
    },
    "electronics": {
        "items": {},
        "title": "Electronics",
        "subtitle": "Discover computers, cameras, TVs, and more.",
    },
}
