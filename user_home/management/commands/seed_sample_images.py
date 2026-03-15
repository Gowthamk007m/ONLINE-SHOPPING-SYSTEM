from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ad_banner.models import Advertisement
from admin_brand.models import Brand
from admin_category.models import Categories
from admin_products.models import Product, Product_Image
from admin_variant.models import Colors, Product_Variant, Variant_images
from user_home.models import CustomUser


class Command(BaseCommand):
    help = "Seed DB with richer image-backed sample records (users, categories, brands, banners, products, variants)."

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        static_root = Path(settings.BASE_DIR) / "static"

        def copy_from_static(static_rel_path: str, upload_to: str, filename: str) -> str:
            src = static_root / static_rel_path
            if not src.exists():
                raise CommandError(f"Missing static source image: {src}")

            target_dir = media_root / upload_to
            target_dir.mkdir(parents=True, exist_ok=True)

            target_name = f"seed_{filename}"
            target = target_dir / target_name
            if not target.exists():
                target.write_bytes(src.read_bytes())

            return f"{upload_to}/{target_name}"

        def download_image(url: str, upload_to: str, filename: str, fallback_static: str | None = None) -> str:
            target_dir = media_root / upload_to
            target_dir.mkdir(parents=True, exist_ok=True)

            target_name = f"seed_{filename}"
            target = target_dir / target_name
            if target.exists():
                return f"{upload_to}/{target_name}"

            try:
                with urlopen(url, timeout=20) as response:
                    image_bytes = response.read()
                    if not image_bytes:
                        raise CommandError(f"Downloaded empty image from {url}")
                    target.write_bytes(image_bytes)
            except (URLError, TimeoutError, OSError) as exc:
                if fallback_static:
                    self.stdout.write(self.style.WARNING(f"Could not download {url}; using fallback static image."))
                    return copy_from_static(fallback_static, upload_to, filename)
                raise CommandError(f"Failed downloading image from {url}: {exc}") from exc

            return f"{upload_to}/{target_name}"

        # Users with internet-backed avatars
        users = [
            {
                "email": "sample.user1@example.com",
                "username": "sampleuser1",
                "phone": "9000000001",
                "image_url": "https://picsum.photos/seed/user-1/400/400",
            },
            {
                "email": "sample.user2@example.com",
                "username": "sampleuser2",
                "phone": "9000000002",
                "image_url": "https://picsum.photos/seed/user-2/400/400",
            },
            {
                "email": "sample.user3@example.com",
                "username": "sampleuser3",
                "phone": "9000000003",
                "image_url": "https://picsum.photos/seed/user-3/400/400",
            },
        ]

        for idx, user_data in enumerate(users, start=1):
            user, _ = CustomUser.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "username": user_data["username"],
                    "phone": user_data["phone"],
                },
            )
            if not user.password:
                user.set_unusable_password()

            if not user.user_image:
                user.user_image.name = download_image(
                    url=user_data["image_url"],
                    upload_to="users",
                    filename=f"user-{idx}.jpg",
                    fallback_static="user_home/images/user-profile.jpg",
                )
                user.save()

        categories = [
            ("Headphones", "https://picsum.photos/seed/category-headphones/800/600", "admin_home/images/Types/on ear.jpg"),
            ("Earbuds", "https://picsum.photos/seed/category-earbuds/800/600", "admin_home/images/Types/tws.jpg"),
            ("Gaming", "https://picsum.photos/seed/category-gaming/800/600", "admin_home/images/Types/gaming.jpg"),
        ]

        category_map = {}
        for name, url, fallback in categories:
            category, _ = Categories.objects.get_or_create(category_name=name)
            if not category.category_image:
                category.category_image.name = download_image(url, "categories", f"{name.lower()}.jpg", fallback)
                category.save()
            category_map[name] = category

        brands = [
            ("Sony", "https://picsum.photos/seed/brand-sony/600/400", "admin_home/images/Logo/sony.jpg"),
            ("JBL", "https://picsum.photos/seed/brand-jbl/600/400", "admin_home/images/Logo/jbl.png"),
            ("boAt", "https://picsum.photos/seed/brand-boat/600/400", "admin_home/images/Logo/boat.png"),
        ]

        brand_map = {}
        for name, url, fallback in brands:
            brand, _ = Brand.objects.get_or_create(brand_name=name)
            if not brand.brand_img:
                brand.brand_img.name = download_image(url, "brand", f"{name.lower()}-brand.jpg", fallback)
                brand.save()
            brand_map[name] = brand

        # One banner/ad per seeded brand
        for idx, (brand_name, brand_obj) in enumerate(brand_map.items(), start=1):
            ad, _ = Advertisement.objects.get_or_create(brand=brand_obj)
            if not ad.ad_image:
                ad.ad_image.name = download_image(
                    url=f"https://picsum.photos/seed/banner-{brand_name.lower()}/1600/600",
                    upload_to="advertisements",
                    filename=f"banner-{idx}.jpg",
                    fallback_static="admin_home/images/ad-1.jpg",
                )
                ad.save()

        # Product catalog with variants
        products = [
            {
                "name": "Sony WH-1000XM5",
                "brand": "Sony",
                "category": "Headphones",
                "description": "Premium wireless ANC headphones with long battery life.",
                "image": "https://picsum.photos/seed/sony-wh1000xm5/900/900",
                "thumbnail": "https://picsum.photos/seed/sony-wh1000xm5-thumb/900/900",
                "variant_gallery": [
                    "https://picsum.photos/seed/sony-wh1000xm5-v1/900/900",
                    "https://picsum.photos/seed/sony-wh1000xm5-v2/900/900",
                ],
                "color": "Black",
                "price": 29999,
                "quantity": 25,
            },
            {
                "name": "JBL Tune 770NC",
                "brand": "JBL",
                "category": "Headphones",
                "description": "Foldable over-ear Bluetooth headphones with active noise cancelling.",
                "image": "https://picsum.photos/seed/jbl-tune-770nc/900/900",
                "thumbnail": "https://picsum.photos/seed/jbl-tune-770nc-thumb/900/900",
                "variant_gallery": [
                    "https://picsum.photos/seed/jbl-tune-770nc-v1/900/900",
                    "https://picsum.photos/seed/jbl-tune-770nc-v2/900/900",
                ],
                "color": "Blue",
                "price": 11999,
                "quantity": 40,
            },
            {
                "name": "boAt Airdopes 141",
                "brand": "boAt",
                "category": "Earbuds",
                "description": "Budget TWS earbuds with low-latency mode and fast charging.",
                "image": "https://picsum.photos/seed/boat-airdopes-141/900/900",
                "thumbnail": "https://picsum.photos/seed/boat-airdopes-141-thumb/900/900",
                "variant_gallery": [
                    "https://picsum.photos/seed/boat-airdopes-141-v1/900/900",
                    "https://picsum.photos/seed/boat-airdopes-141-v2/900/900",
                ],
                "color": "White",
                "price": 1999,
                "quantity": 60,
            },
            {
                "name": "Sony INZONE H9",
                "brand": "Sony",
                "category": "Gaming",
                "description": "Wireless gaming headset with spatial audio and boom mic.",
                "image": "https://picsum.photos/seed/sony-inzone-h9/900/900",
                "thumbnail": "https://picsum.photos/seed/sony-inzone-h9-thumb/900/900",
                "variant_gallery": [
                    "https://picsum.photos/seed/sony-inzone-h9-v1/900/900",
                    "https://picsum.photos/seed/sony-inzone-h9-v2/900/900",
                ],
                "color": "White",
                "price": 22999,
                "quantity": 15,
            },
        ]

        for idx, product_data in enumerate(products, start=1):
            product, _ = Product.objects.get_or_create(
                product_name=product_data["name"],
                defaults={
                    "brand": brand_map[product_data["brand"]],
                    "category": category_map[product_data["category"]],
                    "product_description": product_data["description"],
                },
            )

            product_image = download_image(
                product_data["image"],
                "products",
                f"product-{idx}.jpg",
                fallback_static="admin_home/images/product-1.jpg",
            )
            Product_Image.objects.get_or_create(product=product, image=product_image)

            color, _ = Colors.objects.get_or_create(color_name=product_data["color"])
            variant, created = Product_Variant.objects.get_or_create(
                product=product,
                color=color,
                defaults={
                    "quantity": product_data["quantity"],
                    "price": product_data["price"],
                    "is_available": True,
                },
            )

            if created or not variant.thumbnail:
                variant.thumbnail.name = download_image(
                    product_data["thumbnail"],
                    "variant_thumbnail",
                    f"variant-thumb-{idx}.jpg",
                    fallback_static="admin_home/images/product-2.jpg",
                )
                variant.save()

            for g_idx, gallery_url in enumerate(product_data["variant_gallery"], start=1):
                gallery_img = download_image(
                    gallery_url,
                    "variant_images",
                    f"variant-{idx}-{g_idx}.jpg",
                    fallback_static="admin_home/images/product-3.jpg",
                )
                Variant_images.objects.get_or_create(variant=variant, image=gallery_img)

        self.stdout.write(self.style.SUCCESS("Rich sample image-backed records are seeded successfully."))
