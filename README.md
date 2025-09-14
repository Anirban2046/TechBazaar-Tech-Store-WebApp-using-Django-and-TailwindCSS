# 🛒 TechBazaar: Tech Store WebApp using Django and TailwindCSS

<div align="center">

![TechBazaar Logo](techbazaar/static/images/logo.png)

[![Django](https://img.shields.io/badge/Django-5.2.5-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)

**A comprehensive e-commerce platform built with Django and TailwindCSS, specifically designed for electronic gadgets and tech products**

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🛠️ Technologies Used](#️-technologies-used)
- [⚡ Quick Start](#-quick-start)
- [🔧 Installation & Setup](#-installation--setup)
- [📊 Analytics Dashboard](#-analytics-dashboard)
- [🔒 Authentication System](#-authentication-system)
- [🛒 E-commerce Features](#-e-commerce-features)
- [📱 Responsive Design](#-responsive-design)
- [🌙 Dark Mode Support](#-dark-mode-support)

---

## ✨ Features

### 🛍️ **E-commerce Core Features**
- **Product Management**: Comprehensive product catalog with categories, variations, and real-time inventory tracking
- **Advanced Search & Filtering**: Intelligent product search with live preview suggestions, real-time recommendations, category filters, and price ranges
- **Shopping Cart**: Persistent cart functionality with seamless session management and user association
- **Wishlist System**: Save favorite products for future purchases with full guest user support
- **Order Management**: Complete order lifecycle management from placement to delivery confirmation
- **Payment Integration**: Secure payment processing through SSLCOMMERZ gateway (sandbox mode for testing)
- **Product Reviews & Ratings**: Comprehensive 5-star rating system with authenticated user reviews and verified purchase validation
- **Product Gallery**: Multiple high-resolution product images with zoom functionality
- **Stock Management**: Real-time inventory tracking with automated low stock alerts
- **Category Management**: Hierarchical product categorization with dynamic menu generation

### 👤 **User Management & Authentication**
- **Custom User Model**: Extended Django user model with comprehensive profile management capabilities
- **Email-based Authentication**: Modern, secure login system using email addresses instead of usernames
- **Account Verification**: Mandatory email verification process for new account activation
- **User Profiles**: Detailed user profiles featuring address management and complete order history
- **Password Security**: Robust password reset system with email verification and strong password requirements
- **Account Dashboard**: Personalized dashboard for order tracking, profile management, and password updates
- **Session Management**: Secure session handling with automatic timeout protection
- **Permission System**: Role-based access control system for customers, staff, and administrators

### 📊 **Advanced Analytics & Reporting**
- **Sales Analytics**: Comprehensive sales reporting with detailed revenue tracking by day, month, and year
- **Product Performance**: In-depth analysis of best-selling products and inventory insights
- **Customer Analytics**: Advanced user behavior tracking, registration trends, and demographic analysis
- **Revenue Dashboard**: Real-time business metrics with interactive charts and comprehensive graphs
- **Custom Date Filtering**: Flexible date range selection for detailed period analysis
- **Inventory Reports**: Automated low stock alerts and detailed product availability tracking

### 🎨 **Modern UI/UX & Design**
- **Responsive Design**: Mobile-first architecture ensuring perfect display and functionality across all devices
- **Dark Mode Support**: Complete dark/light theme toggle with manual user preference control and persistent settings
- **Interactive Chatbot**: Built-in FAQ chatbot system for instant customer support and assistance
- **Modern Interface**: Clean, intuitive design with smooth animations, transitions, and micro-interactions
- **TailwindCSS Integration**: Utility-first CSS framework integration via CDN for rapid development and consistent styling
- **Error Handling**: User-friendly error messages and comprehensive validation feedback

### 🔧 **Advanced Technical Features**
- **PDF Invoice Generation**: Automated invoice creation and delivery using WeasyPrint
- **Email Notifications**: Comprehensive SMTP email system with OTP verification for order updates and user account actions
- **OTP Authentication**: Time-limited OTP verification with live countdown timers for account activation and password reset
- **Caching System**: Performance optimization through strategic caching implementation
- **Database Optimization**: Efficient database queries with proper indexing and optimized relationships
- **Admin Panel**: Full-featured Django admin interface for content management
- **Bulk Operations**: Advanced admin tools for bulk product and order management operations
- **Data Validation**: Comprehensive form validation and data integrity checks throughout the application

---

## 🛠️ Technologies Used

### **Backend Technologies**
| Technology | Version | Purpose | Features Used |
|------------|---------|---------|---------------|
| ![Django](https://img.shields.io/badge/-Django-092E20?logo=django&logoColor=white) | 5.2.5 | Web Framework | Models, Views, Templates, Admin, Authentication, Middleware |
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | 3.10+ | Programming Language | OOP, Decorators, Context Managers, Type Hints |
| ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-316192?logo=postgresql&logoColor=white) | Latest | Database | ACID Transactions, Indexing, Foreign Keys, Complex Queries |

### **Frontend Technologies**
| Technology | Version | Purpose | Features Used |
|------------|---------|---------|---------------|
| ![TailwindCSS](https://img.shields.io/badge/-Tailwind_CSS-38B2AC?logo=tailwind-css&logoColor=white) | (CDN) | CSS Framework | Utility Classes, Responsive Design, Dark Mode, Custom Components |
| ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black) | ES6+ | Frontend Logic | DOM Manipulation, Event Handling, AJAX, LocalStorage |
| ![jQuery](https://img.shields.io/badge/-jQuery-0769AD?logo=jquery&logoColor=white) | 3.5.1 | DOM Manipulation | Animations, AJAX Requests, Event Handling |
| ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?logo=html5&logoColor=white) | Latest | Markup | Semantic Elements, Forms, Accessibility |

### **Third-party Services & Libraries**
| Service/Library | Purpose | Implementation |
|----------------|---------|----------------|
| **SSLCOMMERZ (Sandbox)** | Payment Gateway | Sandbox payment integration for Bangladesh market testing |
| **WeasyPrint** | PDF Generation | Invoice and report generation |
| **Pillow** | Image Processing | Image upload, resize, and optimization |
| **python-decouple** | Environment Variables | Secure configuration management |
| **django-widget-tweaks** | Form Enhancement | Advanced form styling and customization |
| **SMTP Email** | Email Service | Order notifications and user verification |
| **Chart.js** | Data Visualization | Analytics dashboard charts and interactive visualizations |
| **Font Awesome 4.7.0 & Feather Icons** | Icon Libraries | Modern iconography throughout the application |
| **Google Fonts (Poppins)** | Typography | Custom web fonts for enhanced design |

### **Development & Deployment Tools**
- **Virtual Environment (venv)**: Dependency isolation and management
- **Git**: Version control and collaborative development
- **Django Admin**: Content management and administration
- **Django Debug Toolbar**: Development debugging and optimization
- **PostgreSQL**: Production-ready database with ACID compliance and advanced features

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- Virtual environment tool (venv/virtualenv)
- PostgreSQL database server

### 🚀 One-Command Setup
```bash
# Clone and setup the entire project
git clone https://github.com/Anirban2046/TechBazaar-Tech-Store-WebApp-using-Django-and-TailwindCSS.git
cd TechBazaar
python -m venv django_env
source django_env/bin/activate  # On Windows: django_env\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your environment variables
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

🎉 **Visit http://127.0.0.1:8000 to see your TechBazaar store!**

---

## 🔧 Installation & Setup

### 1. **Clone the Repository**
```bash
git clone https://github.com/Anirban2046/TechBazaar-Tech-Store-WebApp-using-Django-and-TailwindCSS.git
cd TechBazaar
```

### 2. **Setup Virtual Environment**
```bash
# Create virtual environment
python -m venv django_env

# Activate virtual environment
# On Linux/Mac:
source django_env/bin/activate
# On Windows:
django_env\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Environment Configuration**
Create a `.env` file in the root directory:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration (PostgreSQL - Required for production setup)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=techbazaar_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# SSLCOMMERZ Payment Gateway
STORE_ID=your_sslcommerz_store_id
STORE_PASSWORD=your_sslcommerz_password
SSLCOMMERZ_IS_SANDBOX=True
```

### 5. **Database Setup**
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 6. **Collect Static Files**
```bash
python manage.py collectstatic
```

### 7. **Run Development Server**
```bash
python manage.py runserver
```

### 8. **Access the Application**
- **Frontend**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Analytics Dashboard**: http://127.0.0.1:8000/analytics/

---

## 📊 Analytics Dashboard

### **Comprehensive Business Intelligence Dashboard**
The TechBazaar analytics system delivers deep insights into your e-commerce operations through professional Chart.js visualizations and comprehensive reporting:

#### **Key Performance Indicators (KPIs)**
- **Total Sales Revenue**: Real-time revenue tracking with Bangladeshi Taka (Tk) currency
- **Total Orders**: Complete order count with processing metrics
- **Average Order Value**: Per-transaction analysis for pricing strategies
- **Customer Metrics**: Total customer base and acquisition trends

#### **Interactive Charts & Visualizations**
- **Sales & Orders Trend**: Dual-axis line chart showing revenue and order correlation over time
- **Category Performance**: Doughnut chart displaying sales distribution across product categories
- **Monthly Revenue Trend**: Bar chart tracking revenue patterns by month
- **Order Status Distribution**: Pie chart showing order fulfillment progress (New, Accepted, Completed, Cancelled)
- **Top 5 Products by Revenue**: Horizontal bar chart identifying best-performing products
- **Customer Acquisition**: Line chart monitoring new customer registration trends

#### **Advanced Dashboard Features**
- **Professional Chart.js Integration**: Interactive, responsive charts with hover effects and smooth animations
- **Custom Date Filtering**: Flexible date range selection for detailed period analysis
- **Real-time Data Updates**: Live business metrics without page refresh
- **Gradient Design**: Modern UI with professional color schemes and visual effects
- **Mobile Responsive**: Optimized dashboard access on all devices
- **Export Ready**: Data visualization prepared for business reporting
- **Staff Access Required**: Analytics dashboard accessible only to staff and admin users

---

## 🔒 Authentication System

### **Advanced User Management System**
TechBazaar implements a robust authentication system with enterprise-level security features:

#### **Core Authentication Features**
- **Email-based Login**: Modern authentication using email instead of username
- **Account Verification**: Mandatory email verification for new registrations
- **OTP Security**: Time-limited OTP codes with automatic timeout for enhanced security
- **Password Security**: Strong password requirements with complexity validation
- **Secure Password Reset**: OTP-based password reset with email verification and live timer

#### **User Profile System**
- **Extended User Model**: Custom Django user model with additional fields
- **Profile Management**: Comprehensive user profiles with personal information
- **Order History**: Access to all previous orders and invoices

#### **Security Measures**
- **CSRF Protection**: Cross-site request forgery prevention on all forms
- **Secure Headers**: Implementation of security headers for enhanced protection
- **Input Validation**: Comprehensive data validation and sanitization

#### **User Experience Flow**
```
Registration → Email with OTP → OTP Verification (Live Timer) → Profile Setup → Dashboard Access
Password Reset → Email with OTP → OTP Verification (Timeout Protection) → New Password Setup
```

#### **Role-based Access Control**
- **Customer Role**: Standard shopping and account management features
- **Admin Role**: Full system access with content management capabilities
- **Staff Role**: Limited admin access for customer service operations
- **Superuser**: Complete system control with advanced administrative features

---

## 🛒 E-commerce Features

### **Complete E-commerce Platform**
TechBazaar provides all essential e-commerce functionality with advanced features and seamless user experience:

#### **Product Management System**
- **Rich Product Catalog**: Detailed product information with multiple high-resolution images and comprehensive descriptions
- **Product Variations**: Currently supports color variations with plans for additional variation types
- **Advanced Search**: Intelligent search with live preview suggestions, filters, sorting, and real-time product recommendations
- **Category Hierarchy**: Multi-level product categorization with dynamic navigation and breadcrumb support
- **Inventory Tracking**: Real-time stock management with automated low stock alerts and availability indicators
- **Product Reviews**: Comprehensive 5-star customer rating system with authenticated user reviews and verified purchase requirements
- **Pagination**: Optimized browsing experience with 3 products per page for better performance and user experience
- **Bulk Operations**: Advanced admin tools for managing multiple products simultaneously with batch operations

#### **Shopping Cart & Checkout Process**
- **Persistent Cart**: Cart items automatically saved across sessions and devices for seamless shopping experience
- **Cart Management**: Easy quantity updates, item removal, and cart restoration with real-time price calculations
- **Smart Pricing**: Intelligent shipping cost calculation (free shipping above Tk 5,000, otherwise Tk 150) and automatic total cost determination
- **Payment Integration**: Secure payment processing through SSLCOMMERZ gateway with comprehensive payment options
- **Order Validation**: Automated stock verification and price confirmation before checkout completion
- **Order Confirmation**: Immediate order confirmation with automated email notifications and receipt generation

#### **Order Management & Fulfillment**
- **Order Processing**: Complete order lifecycle management from placement to delivery tracking
- **Status Tracking**: Real-time order status updates with detailed progress information for customers
- **Payment Integration**: Secure SSLCOMMERZ payment gateway integration (sandbox implementation for development)
- **Invoice Generation**: Automated PDF invoice creation and email delivery using WeasyPrint
- **Order History**: Comprehensive order tracking system for both customers and administrators

#### **Wishlist & Favorites**
- **Save for Later**: Comprehensive wishlist functionality with variation support
- **Guest Support**: Full wishlist functionality available for non-registered users
- **Easy Management**: Seamless item movement between cart and wishlist with one-click operations

---

## 📱 Responsive Design

### **Mobile-First Architecture & Design**
TechBazaar is built with a mobile-first approach, ensuring optimal user experience across all devices and screen sizes:

#### **TailwindCSS Implementation**
- **Utility-First CSS**: Rapid development with utility classes via CDN
- **Responsive Grid System**: Flexible layouts that adapt to any screen size
- **Component Consistency**: Reusable components ensuring design consistency
- **CDN Integration**: TailwindCSS included via CDN (suitable for development, not production)
- **Custom Components**: Tailored components for e-commerce specific needs

#### **User Interface Elements**
- **Navigation**: Responsive navigation with mobile hamburger menu and smooth transitions
- **Product Layouts**: Adaptive product grids that optimize for available screen space
- **Form Optimization**: Mobile-optimized form inputs with proper keyboard types
- **Image Handling**: Responsive image scaling with lazy loading and zoom functionality
- **Touch Interactions**: Optimized tap targets and gesture recognition

---

## 🌙 Dark Mode Support

### **Complete Theme System & Dark Mode**
TechBazaar features a comprehensive dark mode implementation that significantly enhances user experience and accessibility:

#### **Theme Detection & Management**
- **Manual Toggle**: Easy theme switching with persistent user preference storage
- **Smooth Transitions**: Animated transitions between light and dark themes
- **Complete Coverage**: All pages, components, and admin panels support both themes
- **Consistent Design**: Carefully crafted color schemes maintaining readability and aesthetics

#### **Technical Implementation**
```javascript
// Advanced theme detection and switching
const themeManager = {
    init() {
        const savedTheme = localStorage.getItem('theme');
        const systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const currentTheme = savedTheme || (systemPreference ? 'dark' : 'light');
        this.applyTheme(currentTheme);
    },
    
    toggle() {
        const currentTheme = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
        this.applyTheme(currentTheme);
        localStorage.setItem('theme', currentTheme);
    }
};
```

#### **User Benefits**
- **Eye Strain Reduction**: Comfortable viewing in low-light conditions
- **Battery Optimization**: Reduced power consumption on OLED displays
- **Personal Preference**: Respects individual user preferences and accessibility needs
- **Modern Experience**: Contemporary web application feel with professional appearance
- **Focus Enhancement**: Improved content focus with reduced visual distractions

#### **Design Considerations**
- **Brand Consistency**: Preserves brand identity across theme variations
- **Image Adaptation**: Smart image handling for different theme contexts
- **Form Styling**: Consistent form element appearance in both themes

---