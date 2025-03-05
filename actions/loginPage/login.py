import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from seleniumbase import BaseCase
from config.settings import settings as cfg


class Login:
    def direct_url(self, sb):
        sb.maximize_window()
        sb.open(cfg.staging_url)
        sb.wait(5)

        sb.type("#signup_email", cfg.gmail)
        sb.wait(5)
        sb.click("#submit_btn")

        for _ in range(60):
            if sb.is_text_visible(
                cfg.staging_name, ".p-ia4_home_header_menu__team_name"
            ):
                break
            sb.wait(1)

        sb.assert_text(
            cfg.staging_name,
            ".p-ia4_home_header_menu__team_name",
            timeout=10,
        )

        sb.wait(10)
