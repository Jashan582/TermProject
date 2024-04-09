import requests
import webbrowser

# CHANGE THE VARIABLE BELOW TO YOUR FLASK URL
FLASK_URL = "http://127.0.0.1:5000"


def http(method, path, data=None, headers=None):
    headers = headers or {'Content-Type': 'application/json'}
    url = FLASK_URL + path
    print(f"Making {method} request to {url}...")
    
    response = requests.request(method, url, json=data, headers=headers)
    
    print("Received status code:", response.status_code)
    return response

def get(path):
    return http("GET", path)

def post(path, data=None):
    return http("POST", path, data)

def put(path, data=None):
    return http("PUT", path, data)

def delete(path):
    return http("DELETE", path)


def process_order(order_id, strategy="adjust"):
    data = {"process": True, "strategy": strategy}
    return put(f"/api/orders/{order_id}", data=data)

def demo():
    print("Adding new products...")
    post("/api/products/", {"name": "burger", "price": 6.99, "available": 50})
    post("/api/products/", {"name": "chips", "price": 3.00, "available": 30})
    post("/api/products/", {"name": "soda", "price": 1.00, "available": 20})
    
    input("Check the web page for new products. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")
    
    print("Creating orders...")
    # OK order
    post("/api/orders/",
        {
            "customer_id": 1,
            "items": [
                {"name": "burger", "quantity": 5},
                {"name": "chips", "quantity": 5},
                {"name": "soda", "quantity": 5}
            ]
        }
    )
    # NOK orders
    post("/api/orders/",
        {
            "customer_id": 6,
            "items": [
                {"name": "burger", "quantity": 100},
            ]
        }
    )
    
    post("/api/orders/",
        {
            "customer_id": 5,
            "items": [
                {"name": "chips", "quantity": 60},
            ]
        }
    )
    
    input("Review the created orders, then press Enter to continue.")
    print("Processing OK order...")
    process_order(11, "adjust")
    print("\n")
    print("ignore process for NOK order")
    process_order(13, "ignore")
    print("\n")
    print("Processing first NOK order with reject strategy...")
    response=process_order(12, "reject")
    if response.status_code == 400:
        print(response.json().get("message"))
        print("\n")


    input("Check the processed orders. Press Enter to continue.")
    
    print("Demonstrating error handling...")
    print("Creating an order with a non-existing product")
    response = post("/api/orders/",
        {
            "customer_id": 4,
            "items": [
                {"name": "something", "quantity": 10}
            ]
        }
    )
    print("Response:")
    
    print("Creating an order with an invalid value")
    response = post("/api/orders/",
        {
            "customer_id": 5,
            "items": [
                {"name": "soda", "quantity": -10}  # Invalid quantity
            ]
        }
    )
    print("Response:")
    
    print("Creating a product with an invalid price")
    response = post("/api/products/", {"name": "air", "price": -1})  # Invalid price
    print("Response:")

if __name__ == "__main__":
    demo()


