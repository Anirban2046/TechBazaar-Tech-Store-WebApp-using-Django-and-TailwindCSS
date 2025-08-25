from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg, Q, F
from orders.models import Order, OrderProduct
from store.models import Product, ReviewRating
from category.models import Category
from accounts.models import Account
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
import json

@staff_member_required
def dashboard(request):
    # --- Filters ---
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    category_id = request.GET.get('category')

    # Base querysets
    orders = Order.objects.filter(is_ordered=True)
    order_products = OrderProduct.objects.filter(ordered=True)
    reviews = ReviewRating.objects.filter(status=True)

    # Apply date filters
    if start_date:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        orders = orders.filter(created_at__date__gte=start_date_obj)
        order_products = order_products.filter(created_at__date__gte=start_date_obj)
        reviews = reviews.filter(created_at__date__gte=start_date_obj)
    if end_date:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        orders = orders.filter(created_at__date__lte=end_date_obj)
        order_products = order_products.filter(created_at__date__lte=end_date_obj)
        reviews = reviews.filter(created_at__date__lte=end_date_obj)
    if category_id:
        order_products = order_products.filter(product__category_id=category_id)

    # --- Enhanced KPI Cards ---
    total_sales = float(orders.aggregate(total=Sum('order_total'))['total'] or 0)
    total_orders = orders.count()
    total_products_sold = order_products.aggregate(total=Sum('quantity'))['total'] or 0
    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    
    # Additional KPIs
    total_customers = orders.values('user').distinct().count()
    total_products = Product.objects.filter(is_available=True).count()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    total_reviews = reviews.count()
    
    # Growth metrics (compared to previous period)
    today = timezone.now().date()
    if start_date and end_date:
        period_days = (end_date_obj - start_date_obj).days
        prev_start = start_date_obj - timedelta(days=period_days)
        prev_end = start_date_obj - timedelta(days=1)
    else:
        period_days = 30
        prev_start = today - timedelta(days=60)
        prev_end = today - timedelta(days=30)
    
    prev_orders = Order.objects.filter(
        is_ordered=True,
        created_at__date__gte=prev_start,
        created_at__date__lte=prev_end
    )
    prev_sales = float(prev_orders.aggregate(total=Sum('order_total'))['total'] or 0)
    prev_order_count = prev_orders.count()
    
    sales_growth = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
    orders_growth = ((total_orders - prev_order_count) / prev_order_count * 100) if prev_order_count > 0 else 0

    # --- Enhanced Charts Data ---
    
    # 1. Sales & Orders Last 30 Days
    thirty_days_ago = today - timedelta(days=29)
    daily_stats = []
    
    for i in range(30):
        date = thirty_days_ago + timedelta(days=i)
        day_orders = orders.filter(created_at__date=date)
        day_sales = float(day_orders.aggregate(total=Sum('order_total'))['total'] or 0)
        day_count = day_orders.count()
        
        daily_stats.append({
            'date': date.strftime('%Y-%m-%d'),
            'sales': day_sales,
            'orders': day_count
        })
    
    sales_labels = [stat['date'] for stat in daily_stats]
    sales_data = [stat['sales'] for stat in daily_stats]
    orders_data = [stat['orders'] for stat in daily_stats]

    # 2. Category Performance
    category_performance = (
        order_products.values('product__category__category_name')
        .annotate(
            total_sales=Sum(F('quantity') * F('product_price')),
            total_quantity=Sum('quantity')
        )
        .order_by('-total_sales')
    )
    category_labels = [c['product__category__category_name'] or 'Uncategorized' for c in category_performance]
    category_sales_data = [float(c['total_sales']) for c in category_performance]
    category_quantity_data = [c['total_quantity'] for c in category_performance]

    # 3. Top 10 Products by Revenue
    top_products_revenue = (
        order_products.values('product__product_name')
        .annotate(
            revenue=Sum(F('quantity') * F('product_price')),
            units_sold=Sum('quantity')
        )
        .order_by('-revenue')[:5]
    )
    top_product_labels = [p['product__product_name'] for p in top_products_revenue]
    top_product_revenue_data = [float(p['revenue']) for p in top_products_revenue]
    top_product_units_data = [p['units_sold'] for p in top_products_revenue]

    # 4. Order Status Distribution
    order_status_dist = orders.values('status').annotate(count=Count('id')).order_by('status')
    status_labels = [s['status'] for s in order_status_dist]
    status_data = [s['count'] for s in order_status_dist]

    # 5. Rating Distribution (Enhanced)
    rating_dist = reviews.values('rating').annotate(count=Count('id')).order_by('rating')
    rating_labels = [f"{r['rating']} Star{'s' if r['rating'] != 1 else ''}" for r in rating_dist]
    rating_data = [r['count'] for r in rating_dist]

    # 6. Monthly Revenue Trend (Last 12 months)
    monthly_revenue = []
    for i in range(12):
        month_start = today.replace(day=1) - timedelta(days=i*30)
        month_start = month_start.replace(day=1)
        if i == 0:
            month_end = today
        else:
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_orders = Order.objects.filter(
            is_ordered=True,
            created_at__date__gte=month_start,
            created_at__date__lte=month_end
        )
        month_sales = float(month_orders.aggregate(total=Sum('order_total'))['total'] or 0)
        
        monthly_revenue.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': month_sales
        })
    
    monthly_revenue.reverse()
    monthly_labels = [m['month'] for m in monthly_revenue]
    monthly_data = [m['revenue'] for m in monthly_revenue]

    # 7. Customer Acquisition (New customers per month)
    customer_acquisition = []
    for i in range(6):
        month_start = today.replace(day=1) - timedelta(days=i*30)
        month_start = month_start.replace(day=1)
        if i == 0:
            month_end = today
        else:
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        new_customers = Account.objects.filter(
            date_joined__date__gte=month_start,
            date_joined__date__lte=month_end
        ).count()
        
        customer_acquisition.append({
            'month': month_start.strftime('%b %Y'),
            'customers': new_customers
        })
    
    customer_acquisition.reverse()
    customer_labels = [c['month'] for c in customer_acquisition]
    customer_data = [c['customers'] for c in customer_acquisition]

    # --- Latest Data ---
    latest_orders = orders.select_related('user').order_by('-created_at')[:8]
    latest_reviews = reviews.select_related('user', 'product').order_by('-created_at')[:8]
    
    # Top customers by spending
    top_customers = (
        orders.values('user__first_name', 'user__last_name', 'user__email')
        .annotate(total_spent=Sum('order_total'), order_count=Count('id'))
        .order_by('-total_spent')[:5]
    )

    # Low stock products
    low_stock_products = Product.objects.filter(
        is_available=True,
        stock__lte=10
    ).order_by('stock')[:5]

    # Recent activity summary
    recent_orders_count = orders.filter(created_at__gte=today - timedelta(days=7)).count()
    recent_reviews_count = reviews.filter(created_at__gte=today - timedelta(days=7)).count()
    recent_customers_count = Account.objects.filter(date_joined__gte=today - timedelta(days=7)).count()

    categories = Category.objects.all()

    context = {
        # KPIs
        'total_sales': f"{total_sales:,.2f}",
        'total_orders': total_orders,
        'total_products_sold': total_products_sold,
        'average_rating': round(average_rating, 2),
        'total_customers': total_customers,
        'total_products': total_products,
        'avg_order_value': f"{avg_order_value:.2f}",
        'total_reviews': total_reviews,
        'sales_growth': round(sales_growth, 1),
        'orders_growth': round(orders_growth, 1),
        
        # Chart data
        'sales_labels': json.dumps(sales_labels),
        'sales_data': json.dumps(sales_data),
        'orders_data': json.dumps(orders_data),
        'category_labels': json.dumps(category_labels),
        'category_sales_data': json.dumps(category_sales_data),
        'category_quantity_data': json.dumps(category_quantity_data),
        'top_product_labels': json.dumps(top_product_labels),
        'top_product_revenue_data': json.dumps(top_product_revenue_data),
        'top_product_units_data': json.dumps(top_product_units_data),
        'status_labels': json.dumps(status_labels),
        'status_data': json.dumps(status_data),
        'rating_labels': json.dumps(rating_labels),
        'rating_data': json.dumps(rating_data),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_data': json.dumps(monthly_data),
        'customer_labels': json.dumps(customer_labels),
        'customer_data': json.dumps(customer_data),
        
        # Tables data
        'latest_orders': latest_orders,
        'latest_reviews': latest_reviews,
        'top_customers': top_customers,
        'low_stock_products': low_stock_products,
        'categories': categories,
        
        # Activity summary
        'recent_orders_count': recent_orders_count,
        'recent_reviews_count': recent_reviews_count,
        'recent_customers_count': recent_customers_count,
    }

    # THIS WAS MISSING - RETURN THE RENDERED TEMPLATE
    return render(request, 'analytics/dashboard.html', context)