import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_amazon_sales_data(n_records=10000):
    """
    Generate synthetic Amazon sales data for EDA
    """
    np.random.seed(42)
    random.seed(42)
    
    # Categories and subcategories
    categories = {
        'Electronics': ['Smartphones', 'Laptops', 'Headphones', 'Tablets', 'Cameras', 'Smart Watches'],
        'Clothing': ['Men\'s Fashion', 'Women\'s Fashion', 'Kids\' Fashion', 'Shoes', 'Accessories'],
        'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Children\'s Books', 'Comics'],
        'Home & Kitchen': ['Furniture', 'Kitchen Appliances', 'Decor', 'Bedding', 'Cookware'],
        'Sports & Outdoors': ['Fitness Equipment', 'Camping Gear', 'Sports Apparel', 'Outdoor Recreation']
    }
    
    # Payment methods
    payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash on Delivery', 'Amazon Pay']
    
    # Customer segments
    customer_segments = ['New', 'Regular', 'Prime', 'Premium']
    
    # Cities (Indian cities for diversity)
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad', 'Ahmedabad']
    
    # Generate data
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(n_records):
        # Random category and subcategory
        category = random.choice(list(categories.keys()))
        subcategory = random.choice(categories[category])
        
        # Price based on category
        if category == 'Electronics':
            price = np.random.uniform(500, 150000)
        elif category == 'Clothing':
            price = np.random.uniform(200, 5000)
        elif category == 'Books':
            price = np.random.uniform(100, 2000)
        elif category == 'Home & Kitchen':
            price = np.random.uniform(300, 30000)
        else:  # Sports & Outdoors
            price = np.random.uniform(500, 20000)
        
        # Quantity (1-5 items)
        quantity = np.random.randint(1, 6)
        
        # Discount based on category and random chance
        discount_percent = np.random.choice([0, 5, 10, 15, 20, 25, 30], p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.08, 0.07])
        discount_amount = (price * quantity * discount_percent) / 100
        
        # Final price after discount
        final_price = (price * quantity) - discount_amount
        
        # Customer rating (3-5 stars, with some 1-2 stars for variety)
        rating = np.random.choice([1, 2, 3, 4, 5], p=[0.02, 0.03, 0.15, 0.4, 0.4])
        
        # Review length indicator
        review_length = np.random.choice(['Short', 'Medium', 'Long'], p=[0.3, 0.5, 0.2])
        
        # Delivery days (1-10 days)
        delivery_days = np.random.randint(1, 11)
        
        # Delivery status
        delivery_status = np.random.choice(['On Time', 'Delayed', 'Early'], p=[0.7, 0.2, 0.1])
        
        # Return status
        return_status = np.random.choice(['No', 'Yes'], p=[0.92, 0.08])
        
        # Customer segment
        customer_segment = random.choice(customer_segments)
        
        # Payment method
        payment_method = random.choice(payment_methods)
        
        # City
        city = random.choice(cities)
        
        # Order date (random date within last year)
        order_date = start_date + timedelta(days=random.randint(0, 365))
        
        # Delivery date
        delivery_date = order_date + timedelta(days=delivery_days)
        
        # Profit margin (20-40% of final price)
        profit_margin = final_price * np.random.uniform(0.2, 0.4)
        
        record = {
            'Order_ID': f'ORD{10000 + i}',
            'Order_Date': order_date.strftime('%Y-%m-%d'),
            'Delivery_Date': delivery_date.strftime('%Y-%m-%d'),
            'Category': category,
            'Subcategory': subcategory,
            'Product_Price': round(price, 2),
            'Quantity': quantity,
            'Discount_Percent': discount_percent,
            'Discount_Amount': round(discount_amount, 2),
            'Final_Price': round(final_price, 2),
            'Payment_Method': payment_method,
            'Customer_Segment': customer_segment,
            'City': city,
            'Customer_Rating': rating,
            'Review_Length': review_length,
            'Delivery_Days': delivery_days,
            'Delivery_Status': delivery_status,
            'Returned': return_status,
            'Profit_Margin': round(profit_margin, 2)
        }
        data.append(record)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add some derived columns
    df['Order_Month'] = pd.to_datetime(df['Order_Date']).dt.month
    df['Order_DayOfWeek'] = pd.to_datetime(df['Order_Date']).dt.dayofweek
    df['Order_Quarter'] = pd.to_datetime(df['Order_Date']).dt.quarter
    
    # Day names for better visualization
    day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
                 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['Order_DayName'] = df['Order_DayOfWeek'].map(day_names)
    
    return df

def save_data():
    """
    Generate and save the data to CSV
    """
    print("Generating Amazon sales data...")
    df = generate_amazon_sales_data(10000)
    
    # Save to CSV
    df.to_csv('amazon_sales_data.csv', index=False)
    print(f"Data saved to amazon_sales_data.csv")
    print(f"Shape of data: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nData Info:")
    print(df.info())
    
    return df

if __name__ == "__main__":
    df = save_data()