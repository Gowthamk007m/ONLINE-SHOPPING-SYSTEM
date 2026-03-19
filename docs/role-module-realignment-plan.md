# Role Module Realignment Plan (Admin / Seller / Buyer)

## Current project state (as implemented)

The current Django project has a strong **admin-oriented back-office** implementation spread across:

- `admin_home`
- `admin_products`
- `admin_category`
- `admin_brand`
- `admin_variant`
- `user_management`
- `ad_banner`

From URL routing and app registration, there is **no dedicated `seller` app/module** yet.

## Recommendation

Your idea is good, but do it in **two phases** so we avoid breaking existing flows:

1. **Phase 1: Treat current admin modules as Seller Console**
   - Keep existing code, but gradually relabel routes/templates/actions that are actually seller responsibilities.
   - Example: product management, order management, payment view, profile.

2. **Phase 2: Build a separate true Admin Console**
   - Implement a new `platform_admin` (or `super_admin`) app aligned to your Level 1 DFD.
   - Responsibilities should be governance-level (view all sellers/buyers/products/orders/payments, policy controls, approvals, audits), not day-to-day selling tasks.

This phased path minimizes risk and lets you ship a seller role quickly.

## Suggested target boundaries (based on your DFD)

### Seller app should own
- View/edit seller profile
- Manage own products (create/update)
- Manage own orders
- View own payouts/payments
- View buyer-facing feedback

### Admin app should own
- View/edit admin profile
- View all sellers
- View all buyers
- View all products
- View all orders
- View all payments
- (Optional) seller approval and account moderation

### Buyer area (already largely present)
- View products
- Order product
- Send feedback
- Send payments
- View/edit profile

## Implementation checklist

1. Introduce role-based namespaces in URLs:
   - `/seller/...`
   - `/admin/...` (platform admin)
   - `/buyer/...` (existing user-facing area)
2. Add role guards/middleware/decorators for each namespace.
3. Reuse existing admin templates first, then split branding/layout.
4. Add seller-specific dashboard metrics (own sales/orders/products only).
5. Create a new admin dashboard with global aggregates and cross-seller reports.
6. Add test coverage for authorization boundaries (seller cannot access global admin data).

## Naming strategy

To reduce churn, avoid hard renaming many apps immediately. Prefer:

- Keep existing app folders for now.
- Expose seller-facing URLs under `/seller/` first.
- Once stable, optionally migrate code into a dedicated `seller` app.

This lowers migration risk and helps keep `git blame` and import paths manageable.

## Final decision

**Yes — your direction is correct.**

- Use today’s “admin” feature set as your **seller console foundation**.
- Build a **separate true admin module** for platform-level operations according to Level 1 DFD.
- Execute in phases to avoid regressions.

## Table changes applied in code (based on your schema images)

To align with your Table 2–7 design, these database-level updates were implemented:

- **Product table**: added `seller` foreign key on `Product`.
- **Orders table**: added order-level `status` field (`pending/completed/cancelled`).
- **Order Items table**: added `subtotal` field, auto-calculated on save.
- **Feedback table**: added new `Feedback` model (`product`, `buyer`, `rating`, `comment`, `created_at`).
- **Payments table**: added new `Payment` model (`order`, `buyer`, `payment_date`, `amount`, `payment_status`, `payment_method`).
- **Admin Reports table**: added new `AdminReport` model (`report_type`, `generated_at`, `report_data` JSON).
