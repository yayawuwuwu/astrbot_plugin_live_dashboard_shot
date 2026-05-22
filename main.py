import os
import traceback
import yaml
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api import AstrBotConfig

CONFIG_PATH = "/AstrBot/data/plugin_configs/live-dashboard-shot.yaml"

@register("live-dashboard-shot", "yayawuwuwu", "对 Live-Dashboard 分设备截图", "1.0.0")
class LiveDashboardShot(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)

        # ========== 双保险：强制读取已保存的配置文件 ==========
        try:
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    file_config = yaml.safe_load(f)
                if file_config and isinstance(file_config, dict):
                    for key, value in file_config.items():
                        config[key] = value  # 更新到 AstrBotConfig 对象
                    logger.info(f"✅ 已从文件加载用户配置: {list(file_config.keys())}")
                else:
                    logger.info("配置文件为空，使用默认值")
            else:
                logger.info(f"配置文件不存在，将在 WebUI 保存后自动生成")
        except Exception as e:
            logger.error(f"手动加载配置文件失败: {e}")
        # =====================================================

        self.config = config
        logger.info(f"当前生效配置: dashboard_url={self.config.get('dashboard_url')}, device_names={self.config.get('device_names')}")

    @filter.command("仪表盘")
    async def cmd_dashboard(self, event: AstrMessageEvent):
        async for msg in self._take_shot(event):
            yield msg

    @filter.command("视奸")
    async def cmd_peep(self, event: AstrMessageEvent):
        async for msg in self._take_shot(event):
            yield msg

    async def _take_shot(self, event: AstrMessageEvent):
        try:
            from playwright.async_api import async_playwright
            from PIL import Image
            import io
        except ImportError:
            yield event.plain_result("截图功能依赖缺失，请先执行 pip install playwright Pillow && playwright install chromium")
            return

        dashboard_url = self.config.get("dashboard_url", "http://172.17.0.1:7283")
        device_names_str = self.config.get("device_names", "芽芽的拯救者y7000\n芽芽的一加ace5至尊版")
        device_names = [n.strip() for n in device_names_str.split("\n") if n.strip()]
        viewport_width = int(self.config.get("viewport_width", 600))
        viewport_height = int(self.config.get("viewport_height", 1000))
        device_scale_factor = int(self.config.get("device_scale_factor", 2))

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page(
                    viewport={"width": viewport_width, "height": viewport_height},
                    device_scale_factor=device_scale_factor,
                )
                await page.goto(dashboard_url, wait_until="networkidle")

                if device_names:
                    first_device = device_names[0]
                    await page.wait_for_selector(f"text={first_device}", timeout=10000)

                img_paths = []
                for idx, name in enumerate(device_names):
                    try:
                        await page.click(f"text={name}", timeout=3000)
                        await page.wait_for_selector(f"text={name}", timeout=5000)
                        await page.wait_for_timeout(1500)
                    except Exception as e:
                        logger.warning(f"无法点击设备 {name}: {e}")
                        continue

                    screenshot_bytes = await page.screenshot(full_page=True)
                    img = Image.open(io.BytesIO(screenshot_bytes))
                    path = f"/tmp/dashboard_{idx}.png"
                    img.save(path, "PNG", optimize=True)
                    img_paths.append(path)

                await browser.close()

            if not img_paths:
                yield event.plain_result("未截取到任何设备信息，请检查设备名称是否正确")
                return

            for path in img_paths:
                yield event.image_result(path)

        except Exception as e:
            logger.error(traceback.format_exc())
            yield event.plain_result(f"截图出错：{e}")
