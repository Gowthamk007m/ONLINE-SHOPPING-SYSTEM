from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django.conf import settings
from django.core.management.base import BaseCommand

from ad_banner.models import Advertisement
from admin_brand.models import Brand
from admin_category.models import Categories
from admin_products.models import Product, Product_Image
from admin_variant.models import Colors, Product_Variant, Variant_images
from user_home.models import CustomUser


class Command(BaseCommand):
    help = "Seed DB with sample records and image files for user/product/category/brand/ad rendering."

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        static_root = Path(settings.BASE_DIR) / "static"

        def copy_from_static(static_rel_path: str, upload_to: str, filename: str) -> str:
            src = static_root / static_rel_path
            if not src.exists():
                raise FileNotFoundError(f"Missing static source image: {src}")

            target_dir = media_root / upload_to
            target_dir.mkdir(parents=True, exist_ok=True)

            target_name = f"seed_{filename}"
            target = target_dir / target_name
            if not target.exists():
                target.write_bytes(src.read_bytes())

            return f"{upload_to}/{target_name}"

        # User image
        user, _ = CustomUser.objects.get_or_create(
            email="sample.user@example.com",
            defaults={
                "username": "sampleuser",
                "phone": "9999999999",
            },
        )
        if not user.password:
            user.set_unusable_password()

        if not user.user_image:
            user.user_image.name = copy_from_static(
                "user_home/images/user-profile.jpg", "users", "user-profile.jpg"
            )
        user.save()

        # Category image
        category, _ = Categories.objects.get_or_create(category_name="Headphones")
        if not category.category_image:
            category.category_image.name = copy_from_static(
                "admin_home/images/Types/on ear.jpg", "categories", "on-ear.jpg"
            )
            category.save()

        # Brand image
        brand, _ = Brand.objects.get_or_create(brand_name="Sony")
        if not brand.brand_img:
            brand.brand_img.name = copy_from_static(
                "admin_home/images/Logo/sony.jpg", "brand", "sony.jpg"
            )
            brand.save()

        # Advertisement image
        ad, _ = Advertisement.objects.get_or_create(brand=brand)
        if not ad.ad_image:
            ad.ad_image.name = copy_from_static(
                "admin_home/images/ad-1.jpg", "advertisements", "ad-1.jpg"
            )
            ad.save()

        # Product + product image
        product, _ = Product.objects.get_or_create(
            product_name="WH-1000XM4",
            defaults={
                "brand": brand,
                "category": category,
                "product_description": "Noise cancelling wireless headphones",
            },
        )

        Product_Image.objects.get_or_create(
            product=product,
            image=copy_from_static(
                "admin_home/images/Sony/WF-1000XM3.png", "products", "wf-1000xm3.png"
            ),
        )

        # Variant + variant images
        color, _ = Colors.objects.get_or_create(color_name="Black")
        variant, created = Product_Variant.objects.get_or_create(
            product=product,
            color=color,
            defaults={"quantity": 20, "price": 19999, "is_available": True},
        )

        if created or not variant.thumbnail:
            variant.thumbnail.name = copy_from_static(
                "admin_home/images/product-1.jpg", "variant_thumbnail", "product-1.jpg"
            )
            variant.save()

        for static_rel, file_name in [
            ("admin_home/images/product-2.jpg", "product-2.jpg"),
            ("admin_home/images/product-3.jpg", "product-3.jpg"),
        ]:
            rel_path = copy_from_static(static_rel, "variant_images", file_name)
            Variant_images.objects.get_or_create(variant=variant, image=rel_path)

        self.stdout.write(self.style.SUCCESS("Sample image-backed records are seeded successfully."))
