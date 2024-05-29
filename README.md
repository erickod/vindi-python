# vindi-gateway-python

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Python client library for the Vindi API.**

## Installation

```bash
pip install vindi-gateway-python
```

## Usage

### Authentication

```python
import vindi

client = vindi.Client(api_key="YOUR_API_KEY")
```

Replace `YOUR_API_KEY` with your actual Vindi API key. You can find your API key in your Vindi account settings.

### Making API Requests

```python
# Get a list of customers
customers = client.customers.list_customers(
    page=1,
    items_per_page=25,
    sort_by="created_at",
    order="asc",
    query="id='123123'",
)

# Create a new customer
customer = client.customers.create_customer(
    name="John Doe",
    email="john.doe@example.com",
)


# Update a customer
customer = client.customers.update_customer(
    customer_id="CUSTOMER_ID",
    name="Jane Doe",
)

# Delete a customer
client.customers.delete_customer(customer_id="CUSTOMER_ID")
```

### Using Resources

The `vindi-gateway-python` library provides convenient access to all Vindi API resources:

- `customers`
- `bills`
- `products`
- `payment_methods`
- `subscriptions`
- `webhooks`
- `invoices`

Each resource has its own set of methods for interacting with the corresponding API endpoint.

See the [API documentation](https://vindi.github.io/api-docs/dist/) for a complete list of available resources and methods.

## Example

```python
import vindi

# Create a client instance
client = vindi.Client(api_key="YOUR_API_KEY")

# Create a new customer
customer = client.customers.create_customer(
    name="John Doe",
    email="john.doe@example.com",
)

# Create a new product
product = client.products.create_product(
    name="My Product",
    price=100,
)

# Create a new bill
bill = client.bills.create_bill(
    customer_id=customer.id,
    bill_items=[
        {
            "product_id": product.id,
            "quantity": 1,
        },
    ],
)

# Print the bill information
print(bill)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

```markdown
**Remember to:**

- Replace placeholders like `YOUR_API_KEY` with actual values.
- Include relevant information about your project, such as features, installation instructions, and examples.
- Add more detail to the documentation based on the specific functionality of your library.
- Consider adding badges to your README.md to showcase the project's health and status (like CI/CD, code coverage, license, and version).

Let me know if you have any other questions or need further assistance!
```
