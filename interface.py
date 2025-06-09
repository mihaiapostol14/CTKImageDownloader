import os
import logging
import platform
import subprocess
from pathlib import Path

import flet as ft
from icrawler.builtin import BingImageCrawler
from helper import Helper


class ImageDownloader(Helper):
    def __init__(self, page: ft.Page):
        self.page = page

        self.search_entry = None
        self.max_count_entry = None
        self.output_dir_entry = None
        self.count_image_label = None
        self.download_button = None
        self.open_dir_button = None

        self.search_query = None
        self.image_limit = None

        # ==============================
        # Colors
        # ==============================
        self.colors = {
            "primary": ft.Colors.BLUE,
            "success": ft.Colors.GREEN,
            "error": ft.Colors.RED,
            "text": ft.Colors.WHITE,
            "background": ft.Colors.WHITE,
            "button": ft.Colors.BLUE,
            "button_text": ft.Colors.WHITE,
        }

        # Default output directory
        self.default_output_dir = Path.home() / "Downloads"
        self.output_directory = self.default_output_dir

        print(
            f"[Info] Default output directory: "
            f"{self.output_directory}"
        )

        # FilePicker
        self.folder_picker = ft.FilePicker()

        # Add FilePicker as a page service
        self.page.services.append(self.folder_picker)

        self.page.title = "FletImageDownloader"

        self.page.window.width = 400
        self.page.window.height = 450
        self.page.window.icon = "../assets/icon/icon.ico"
        self.page.window.resizable = False
        self.page.window.maximizable = False

        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # Register keyboard event
        self.page.on_keyboard_event = self.keyboard_input

    def show_message(self, message, color=None):
        """
        Displays a SnackBar notification.
        """

        if color is None:
            color = self.colors["success"]

        snack_bar = ft.SnackBar(
            content=ft.Text(
                message,
                color=ft.Colors.WHITE,
            ),
            bgcolor=color,
        )

        self.page.show_dialog(snack_bar)
        self.page.update()

    async def keyboard_input(self, e):
        # Enter -> Download
        if e.key in ["Enter", "Numpad Enter"]:
            await self.download_image(None)

        # Ctrl + O -> Select output directory
        elif e.ctrl and e.key.lower() == "o":
            await self.select_output_directory()

    async def create_widgets(self):
        # UI Title Label
        title_label = ft.Text(
            "FletImageDownloader",
            size=20,
            color=self.colors["text"],
        )

        # Input entry for search term
        self.search_entry = ft.TextField(
            label="Search Image",
            width=300,
            on_submit=self.download_image,
        )

        # Input entry for maximum image count
        self.max_count_entry = ft.TextField(
            label="Image Count",
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.NumbersOnlyInputFilter(),
            on_submit=self.download_image,
        )

        # Output directory input
        self.output_dir_entry = ft.TextField(
            label="Download Folder",
            value=str(self.output_directory),
            width=260,
        )

        # Folder picker button
        select_folder_button = ft.IconButton(
            icon=ft.Icons.FOLDER_OPEN,
            tooltip="Select Download Folder",
            on_click=self.select_output_directory,
            icon_color=self.colors["primary"],
        )

        # Label for displaying downloaded count
        self.count_image_label = ft.Text(
            value="",
            size=20,
            color=self.colors["text"],
        )

        # Download button
        self.download_button = ft.ElevatedButton(
            "Download",
            on_click=self.download_image,
            width=300,
            bgcolor=self.colors["button"],
            color=self.colors["button_text"],
        )

        # Open directory button
        self.open_dir_button = ft.ElevatedButton(
            "Open",
            on_click=self.open_output_directory,
            width=300,
            bgcolor=self.colors["button"],
            color=self.colors["button_text"],
        )

        self.page.add(
            ft.Column(
                [
                    title_label,
                    self.search_entry,
                    self.max_count_entry,

                    # Download folder + folder picker
                    ft.Row(
                        [
                            self.output_dir_entry,
                            select_folder_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5,
                    ),

                    self.count_image_label,
                    self.download_button,
                    self.open_dir_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
        )

        self.page.update()

    async def select_output_directory(self):
        """
        Opens the native OS directory picker and saves
        the selected directory to the output directory input.
        """

        selected_directory = await self.folder_picker.get_directory_path(
            dialog_title="Select Download Folder",
            initial_directory=str(self.output_directory),
        )

        if selected_directory:
            self.output_directory = Path(selected_directory)

            # Update path input
            self.output_dir_entry.value = str(
                self.output_directory
            )

            self.show_message(
                f"Folder selected: {self.output_directory}",
                self.colors["success"],
            )

            self.page.update()

    async def download_image(self, e):
        """
        Fetches user inputs, validates search arguments,
        and starts BingImageCrawler.
        """

        # Get cleaned user inputs
        self.search_query = self.search_entry.value.strip()
        self.image_limit = self.max_count_entry.value.strip()

        # Validate input criteria
        if not self.search_query or not self.image_limit.isdigit():
            self.show_message(
                "Search text or image count is invalid.",
                self.colors["error"],
            )
            return

        # Get directory from input
        if self.output_dir_entry.value:
            input_path = self.output_dir_entry.value.strip()

            # Check if path is absolute
            if os.path.isabs(input_path):
                input_path = Path(input_path)

                try:
                    input_path.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                    self.output_directory = input_path

                except (OSError, ValueError):
                    self.output_directory = (
                        self.default_output_dir
                    )

                    self.output_dir_entry.value = str(
                        self.default_output_dir
                    )

                    self.show_message(
                        "Invalid path. Using default Downloads folder.",
                        self.colors["error"],
                    )

            else:
                # Relative path -> fallback to default
                self.output_directory = (
                    self.default_output_dir
                )

                self.output_dir_entry.value = str(
                    self.default_output_dir
                )

                self.show_message(
                    "Invalid path. Using default Downloads folder.",
                    self.colors["error"],
                )

        # Prepare storage directory path
        output_directory = (
            self.output_directory / self.search_query
        )

        try:
            # Create directory if it doesn't exist
            output_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.show_message(
                f"Folder ready: {output_directory}",
                self.colors["success"],
            )

            print(
                f"Starting download for query: "
                f"'{self.search_query}'..."
            )

            print(
                f"Output directory: "
                f"'{output_directory}'"
            )

            # Initialize BingImageCrawler instance
            crawler = BingImageCrawler(
                downloader_threads=4,
                storage={
                    "root_dir": str(output_directory)
                },
                log_level=logging.INFO,
            )

            # Start downloading images
            crawler.crawl(
                keyword=self.search_query,
                max_num=int(self.image_limit),
            )

            self.show_message(
                "Download finished successfully.",
                self.colors["success"],
            )

            # Update count status
            self.count_image()

        except Exception as error:
            print(
                f"[Error] Failed to complete crawl operation: "
                f"{error}"
            )

            self.show_message(
                f"Download failed: {error}",
                self.colors["error"],
            )

    def count_image(self):
        """
        Updates UI text with the total number of
        downloaded images in the folder.
        """

        if not self.search_query:
            return

        output_directory = (
            self.output_directory / self.search_query
        )

        if output_directory.exists():
            downloaded_files = len(
                os.listdir(output_directory)
            )

            self.count_image_label.value = (
                f"Count image {self.search_query} "
                f"is {downloaded_files}"
            )

            self.open_dir_button.text = (
                f"Open {self.search_query}"
            )

            self.page.update()

    async def open_output_directory(self, e):
        """
        Opens the downloaded folder using the
        native system file explorer.
        """

        if not self.search_query:
            return

        folder_path = (
            self.output_directory / self.search_query
        ).resolve()

        if not folder_path.exists():
            self.show_message(
                "Download folder does not exist.",
                self.colors["error"],
            )
            return

        try:
            if platform.system() == "Windows":
                os.startfile(folder_path)

            elif platform.system() == "Darwin":
                subprocess.Popen(
                    ["open", str(folder_path)]
                )

            else:
                subprocess.Popen(
                    ["xdg-open", str(folder_path)]
                )

        except Exception as error:
            print(
                f"[Error] Failed to open directory: "
                f"{error}"
            )

            self.show_message(
                f"Failed to open directory: {error}",
                self.colors["error"],
            )


class App:
    async def main(self, page: ft.Page):
        downloader = ImageDownloader(page)
        await downloader.create_widgets()


if __name__ == "__main__":
    ft.app(target=App().main)
