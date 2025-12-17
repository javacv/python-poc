# background_executor.py

from concurrent.futures import ThreadPoolExecutor

background_executor = ThreadPoolExecutor(
    max_workers=10,
    thread_name_prefix="bg-worker"
)