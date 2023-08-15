# OpenAI API

In this repo, there is a Flask API that calls OpenAI's GPT-3.5-Turbo to rephrase or generate text. Due to the possibility of having multiple sections in the API call, all sections are called in parallel.

## How to launch

Build the docker image:

```bash
docker build -t openai_api .
```

Afterwards, run the image:

```bash
docker run -p 5000:5000 openai_api
```

This will run the Flask API on localhost:5000.

There is also an .env file with "openai_key", which is your OpenAI API key, and "api_key" which is the key for this API (by default "api_key").

## Using the API

### The /Rephrase API

It expects JSON with text and a number of variants you want to rephrase.

Example JSON:

```json
{ "text": "some text to rephrase", "number_of_variants": 2 }
```

You can call this function with programs like Postman or curl. You can use this curl command:

```bash
curl -X GET http://localhost:5000/Rephrase -H "Content-Type: application/json" -H "Authorization: Bearer api_key" --data "{\"text\": \"This product is very very good \", \"number_of_variants\":2}"
```

It will return:

```json
["This product is extremely excellent.", "This product is excellent."]
```

### The /Generate API

It expects a description of the company, followed by sections detailing the pages and the content inside those pages to generate.

```json
{
  "description": "company description",
  "sections": {
    "about": { "title": 1, "description": 2 },
    "refund": { "title": 2, "description": 1 },
    "hero": { "title": 1, "description": 1 }
  }
}
```

The numbers represent how many variations it should generate for each item.

For example, if you pass this JSON:

```json
{
  "description": "An ice cream shop",
  "sections": {
    "about": { "title": 2, "description": 1 },
    "refund": { "title": 1, "description": 1 }
  }
}
```

With this curl command:

```bash
curl -X GET http://localhost:5000/Generate -H "Content-Type: application/json" -H "Authorization: Bearer api_key" --data "{\"description\": \"An ice cream shop \", \"sections\":{ \"about\": {\"title\":2, \"description\":1}, \"refund\":{\"title\":1, \"description\":1} } } "
```

It returns:

```json
{
  "about": {
    "title": [
      "The Scoop: Discover Our Delicious Frozen Creations and Sweet Indulgences",
      "Indulge in Blissful Delights: Unveiling the Frosty Delights of Our Artisanal Ice Cream Shop"
    ],
    "description": [
      "Welcome to our delightful ice cream haven! Our ice cream shop is a dreamy paradise for all ice cream enthusiasts. Indulge in our handcrafted frozen treats that will transport your taste buds to a world of pure bliss. Each scoop is made with love and passion, using only the finest ingredients, ensuring the smoothest, creamiest ice cream experience. From classic flavors to exotic creations, there's something to satisfy every craving. With our charming ambiance and friendly service, we aim to create unforgettable moments and spread joy one scoop at a time. Come and join us for a delightful journey through the wonders of ice cream."
    ]
  },
  "refund": {
    "title": [
      "Sweet Satisfaction Guaranteed: Our Hassle-Free Ice Cream Refund Policy"
    ],
    "description": [
      "Welcome to our ice cream shop's refund page, where your satisfaction is our top priority! We understand that sometimes things don't go as planned, and we're here to make it right. If you're not 100% satisfied with your ice cream experience, we offer a hassle-free refund process. Simply reach out to our friendly team within [X] days of your purchase, and we'll gladly assist you. Whether it's an issue with the flavor, texture, or any other concern, we're committed to ensuring that every scoop brings a smile to your face. Your happiness is the cherry on top of our ice cream!"
    ]
  }
}
```
