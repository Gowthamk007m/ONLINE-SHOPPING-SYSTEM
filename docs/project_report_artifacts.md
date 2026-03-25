# BuyNow Project Report Artifacts

This document provides ready-to-use **DFDs**, **ERD**, and supporting report tables/diagrams for the BuyNow Django e-commerce system.

---

## 1) Project Summary Table

| Item | Details |
|---|---|
| Project Name | BuyNow |
| Project Type | Web-based E-commerce Platform |
| Tech Stack | Django, SQLite/PostgreSQL-ready models, HTML/CSS/Bootstrap, Razorpay integration |
| Main Users | Customer, Admin, Seller (via product ownership), Payment Gateway |
| Core Domains | Authentication, Catalog, Cart, Checkout, Orders, Payments, Wishlist, Reviews, Coupons |

---

## 2) Actor & Responsibility Table

| Actor | Responsibilities |
|---|---|
| Customer | Register/login, browse products, add to cart/wishlist, checkout, place/cancel orders, view invoice |
| Admin | Manage brands/categories/products/variants, monitor users, manage offers/coupons, track reports |
| Seller (logical role) | Adds/manages owned products and variants |
| Payment Gateway (Razorpay) | Creates/authorizes payment transactions and returns payment metadata |
| Notification Services | Sends OTP/email/SMS alerts |

---

## 3) Functional Requirements Table

| ID | Requirement |
|---|---|
| FR-01 | User registration and OTP-based verification |
| FR-02 | Secure login/logout and blocked-user handling |
| FR-03 | Product catalog with brand/category/variant support |
| FR-04 | Cart operations with quantity and coupon discount |
| FR-05 | Checkout with address selection and payment method |
| FR-06 | Order creation with item-level status tracking |
| FR-07 | Payment recording and status tracking |
| FR-08 | Wishlist and product review/feedback |
| FR-09 | Admin management for inventory and users |
| FR-10 | Invoice generation and order history |

---

## 4) Non-Functional Requirements Table

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Usability | Simple storefront + admin UI |
| NFR-02 | Reliability | Order/payment records persisted transactionally |
| NFR-03 | Security | Authenticated routes, OTP verification, role-based admin controls |
| NFR-04 | Performance | Product browsing and cart operations should be responsive for standard workloads |
| NFR-05 | Maintainability | Modular Django apps by domain |

---

## 5) Data Flow Diagram (DFD) — Level 0 (Context)

```mermaid
flowchart LR
    C[Customer] -->|Register/Login, Browse, Cart, Checkout| S((BuyNow System))
    A[Admin] -->|Manage Catalog/Users/Reports| S
    S -->|Pages, Order Status, Invoice, Notifications| C
    S -->|Dashboards, Reports| A
    S <--> |Payment Request/Response| P[Payment Gateway]
    S <--> |Email/SMS OTP| N[Notification Services]
    S <--> |CRUD Data| D[(Application Database)]
```

---

## 6) Data Flow Diagram (DFD) — Level 1

```mermaid
flowchart TB
    C[Customer]
    A[Admin]
    PG[Payment Gateway]
    NS[Notification Services]

    P1((1.0 User & Auth))
    P2((2.0 Catalog Management))
    P3((3.0 Cart & Wishlist))
    P4((4.0 Checkout & Orders))
    P5((5.0 Payment Processing))
    P6((6.0 Reviews & Feedback))
    P7((7.0 Reporting))

    D1[(User DB)]
    D2[(Catalog DB)]
    D3[(Cart/Wishlist DB)]
    D4[(Order DB)]
    D5[(Payment DB)]
    D6[(Review DB)]

    C --> P1
    P1 --> NS
    P1 <--> D1

    C --> P2
    A --> P2
    P2 <--> D2

    C --> P3
    P3 <--> D3
    P3 <--> D2

    C --> P4
    P4 <--> D4
    P4 <--> D3
    P4 <--> D1

    P4 --> P5
    P5 <--> PG
    P5 <--> D5
    P5 --> D4

    C --> P6
    P6 <--> D6
    P6 <--> D2

    A --> P7
    P7 <--> D1
    P7 <--> D2
    P7 <--> D4
    P7 <--> D5
```

---

## 7) Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    CUSTOM_USER ||--o{ USER_ADDRESS : has
    CUSTOM_USER ||--o{ USER_OTP : verifies
    CUSTOM_USER ||--o{ MOBILE_OTP : verifies
    CUSTOM_USER ||--o{ CART : owns
    CUSTOM_USER ||--o{ ORDER : places
    CUSTOM_USER ||--o{ ORDER_ITEM : receives
    CUSTOM_USER ||--o{ PAYMENT : makes
    CUSTOM_USER ||--o{ WISHLIST : maintains
    CUSTOM_USER ||--o{ REVIEW_RATING : writes
    CUSTOM_USER ||--o{ FEEDBACK : writes

    BRAND ||--o{ PRODUCT : classifies
    CATEGORY ||--o{ PRODUCT : classifies
    PRODUCT ||--o{ PRODUCT_IMAGE : has
    PRODUCT ||--o{ PRODUCT_VARIANT : has
    COLOR ||--o{ PRODUCT_VARIANT : colors
    PRODUCT_VARIANT ||--o{ VARIANT_IMAGE : has

    COUPON ||--o{ CART : applies_to

    CART ||--o{ CART_ITEM : contains
    PRODUCT_VARIANT ||--o{ CART_ITEM : selected_as

    USER_ADDRESS ||--o{ ORDER : used_in
    PAYMENT_METHODS ||--o{ ORDER : chosen_for
    ORDER ||--o{ ORDER_ITEM : contains
    PRODUCT_VARIANT ||--o{ ORDER_ITEM : ordered_as

    ORDER ||--o{ PAYMENT : has

    PRODUCT ||--o{ REVIEW_RATING : reviewed_in
    PRODUCT ||--o{ FEEDBACK : feedback_in

    BRAND ||--o{ ADVERTISEMENT : promoted_by
```

---

## 8) Use Case Diagram

```mermaid
flowchart LR
    Customer((Customer))
    Admin((Admin))

    UC1([Register/Login])
    UC2([Verify OTP])
    UC3([Browse/Search Products])
    UC4([Manage Cart/Wishlist])
    UC5([Checkout])
    UC6([Make Payment])
    UC7([Track/Cancel Order])
    UC8([Review Product])

    UA1([Manage Brands/Categories])
    UA2([Manage Products/Variants])
    UA3([Manage Users])
    UA4([Manage Coupons/Banners])
    UA5([Generate Reports])

    Customer --- UC1
    Customer --- UC2
    Customer --- UC3
    Customer --- UC4
    Customer --- UC5
    Customer --- UC6
    Customer --- UC7
    Customer --- UC8

    Admin --- UA1
    Admin --- UA2
    Admin --- UA3
    Admin --- UA4
    Admin --- UA5
```

---

## 9) Activity Diagram — Order Placement

```mermaid
flowchart TD
    Start([Start]) --> Login{Logged in?}
    Login -- No --> DoLogin[Login/Register + OTP Verify]
    DoLogin --> Browse
    Login -- Yes --> Browse[Browse Products]
    Browse --> Select[Select Variant & Quantity]
    Select --> AddCart[Add to Cart]
    AddCart --> Coupon{Apply Coupon?}
    Coupon -- Yes --> ApplyCoupon[Validate & Apply]
    Coupon -- No --> Address
    ApplyCoupon --> Address[Select/Create Address]
    Address --> PaymentMethod[Choose Payment Method]
    PaymentMethod --> Payment{Online Payment?}
    Payment -- Yes --> Gateway[Process via Razorpay]
    Gateway --> Success{Payment Success?}
    Success -- No --> Fail[Mark Failed/Pending & Retry]
    Success -- Yes --> CreateOrder
    Payment -- No --> CreateOrder[Create Order + Order Items]
    CreateOrder --> Invoice[Generate Invoice]
    Invoice --> End([End])
    Fail --> End
```

---

## 10) Sequence Diagram — Checkout & Payment

```mermaid
sequenceDiagram
    participant U as Customer
    participant W as Web App (Django)
    participant DB as Database
    participant PG as Razorpay

    U->>W: Checkout request
    W->>DB: Fetch cart + address + totals
    DB-->>W: Cart data
    W-->>U: Show payment options

    U->>W: Confirm order (online)
    W->>PG: Create payment order
    PG-->>W: payment_order_id
    W-->>U: Launch payment UI
    U->>PG: Complete payment
    PG-->>W: payment_id + signature

    W->>DB: Save Order, OrderItems, Payment
    DB-->>W: Persisted
    W-->>U: Order success + invoice
```

---

## 11) Deployment Diagram (Logical)

```mermaid
flowchart LR
    UserDevice[User Browser/Mobile] --> WebServer[Django App Server]
    AdminDevice[Admin Browser] --> WebServer
    WebServer --> StaticMedia[(Static/Media Storage)]
    WebServer --> AppDB[(SQLite/PostgreSQL)]
    WebServer <--> Razorpay[Razorpay API]
    WebServer <--> Notify[SMTP/Twilio]
```

---

## 12) Data Dictionary (Core Tables)

### 12.1 User/Auth Domain

| Table | Key Fields |
|---|---|
| `CustomUser` | `id`, `email`, `username`, `phone`, `wallet`, `is_blocked`, `identification` |
| `UserOTP` | `id`, `user_id`, `otp`, `time_st` |
| `Mobile_Otp` | `id`, `user_id`, `otp`, `time_st` |
| `User_Address` | `id`, `user_id`, `fullname`, `contact_number`, `house_name`, `city`, `state`, `pincode` |

### 12.2 Catalog Domain

| Table | Key Fields |
|---|---|
| `Brand` | `id`, `brand_id`, `brand_name`, `brand_img` |
| `Categories` | `id`, `category_name`, `category_image` |
| `Product` | `id`, `identification`, `product_name`, `seller_id`, `brand_id`, `category_id` |
| `Product_Image` | `id`, `product_id`, `image` |
| `Colors` | `id`, `color_name` |
| `Product_Variant` | `id`, `product_id`, `color_id`, `quantity`, `price`, `is_available`, `thumbnail` |
| `Variant_images` | `id`, `variant_id`, `image` |
| `Advertisement` | `id`, `brand_id`, `ad_image` |

### 12.3 Cart/Order/Payment Domain

| Table | Key Fields |
|---|---|
| `Coupon` | `id`, `name`, `min_amount`, `off_percent`, `max_discount`, `quantity`, `expiry_date`, `status` |
| `Cart` | `id`, `cart_id`, `user_id`, `coupon_id`, `coupon_discount`, `status` |
| `CartItem` | `id`, `cart_id`, `variant_id`, `qty` |
| `Payment_methods` | `id`, `method` |
| `Order` | `id`, `order_id`, `customer_id`, `address_id`, `total`, `coupon`, `payment_method_id`, `status` |
| `Order_item` | `id`, `order_id`, `variant_id`, `user_id`, `quantity`, `subtotal`, `status` |
| `Payment` | `id`, `order_id`, `buyer_id`, `amount`, `payment_status`, `payment_method`, `payment_date` |

### 12.4 Engagement/Reporting Domain

| Table | Key Fields |
|---|---|
| `Wishlist` | `id`, `user_id`, `variant_id`, `date_added` |
| `ReviewRating` | `id`, `user_id`, `product_id`, `review`, `rating`, `status` |
| `Feedback` | `id`, `buyer_id`, `product_id`, `rating`, `comment`, `created_at` |
| `AdminReport` | `id`, `report_type`, `generated_at`, `report_data` |

---

## 13) Report-Ready Notes

- These Mermaid blocks can be pasted directly into Markdown renderers that support Mermaid (GitHub, many documentation tools).
- If your college/report template requires images, render these diagrams to PNG/SVG and insert them under corresponding chapters (System Design, Database Design, Process Design).
- Suggested chapter mapping:
  1. System Overview → Sections 1–4
  2. DFDs → Sections 5–6
  3. Database Design → Sections 7 and 12
  4. Behavioral Design → Sections 8–10
  5. Deployment/Implementation View → Section 11
