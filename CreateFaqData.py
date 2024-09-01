import pandas as pd

# Define the FAQ data
faq_data = {
    "question": [
        "What are your business hours?",
        "How can I reset my password?",
        "What is your return policy?",
        "How do I contact customer support?",
        "Where can I find product information?",
        "Do you offer international shipping?",
        "How can I track my order?",
        "What payment methods do you accept?",
        "Can I change my order after it has been placed?",
        "How do I unsubscribe from the newsletter?"
    ],
    "answer": [
        "We are open from 9 AM to 5 PM, Monday to Friday.",
        "You can reset your password by clicking on 'Forgot Password' on the login page.",
        "Our return policy allows returns within 30 days of purchase.",
        "You can contact customer support via email at support@example.com or call us at 1-800-555-0199.",
        "Product information can be found on the product page on our website.",
        "Yes, we offer international shipping to select countries.",
        "You can track your order using the tracking link provided in your confirmation email.",
        "We accept Visa, MasterCard, American Express, and PayPal.",
        "Yes, you can change your order by contacting customer support before it ships.",
        "To unsubscribe, click the 'unsubscribe' link at the bottom of our emails."
    ]
}

# Create a DataFrame from the FAQ data
faq_df = pd.DataFrame(faq_data)

# Save the DataFrame to a CSV file
faq_df.to_csv('faq_data.csv', index=False)

print("FAQ data CSV file created successfully.")