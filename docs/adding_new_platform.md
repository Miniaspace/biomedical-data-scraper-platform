# Guide: Adding a New Platform

This guide provides a step-by-step walkthrough for adding a new data source (platform) to the scraping platform.

## Prerequisites

- You have a local development environment set up (see `README.md`).
- You have analyzed the target platform to understand its structure, pagination, and data fields.

## Step 1: Use the Scaffolding Script

The easiest way to start is by using the `add_platform.py` script. This will create the necessary files and configuration templates for you.

1.  **Run the script** from the project root directory:

    ```bash
    python scripts/add_platform.py <platform_name>
    ```

    Replace `<platform_name>` with a short, lowercase, snake_case name for the new platform (e.g., `my_new_platform`).

2.  **Follow the prompts**: The script will ask for information like the display name, base URL, and authentication requirements. Provide these details.

3.  **Review the output**: The script will create:
    - A new spider file: `spiders/my_new_platform_spider.py`
    - A new entry in `config/platforms.yaml`

## Step 2: Implement the Spider Logic

Now, open the newly created spider file (`spiders/my_new_platform_spider.py`). You need to implement the two main parsing methods.

### 2.1. `parse_list_page(self, response)`

This method is responsible for finding links to the individual detail pages from a list or search results page.

-   **Identify the CSS or XPath selector** that uniquely identifies the links to the detail pages.
-   **Loop through the links** and yield a `scrapy.Request` for each one, calling `self.parse_detail_page` as the callback.
-   **Handle pagination**: Find the link to the next page and yield a request to it, calling `self.parse_list_page` as the callback.

**Example:**

```python
def parse_list_page(self, response: Response) -> Iterator[Request]:
    # Extract links to detail pages
    detail_links = response.css("div.study-item a.title::attr(href)").getall()
    for link in detail_links:
        yield scrapy.Request(
            url=response.urljoin(link),
            callback=self.parse_detail_page
        )

    # Handle pagination
    next_page = response.css("a.pagination-next::attr(href)").get()
    if next_page:
        yield scrapy.Request(
            url=response.urljoin(next_page),
            callback=self.parse_list_page
        )
```

### 2.2. `parse_detail_page(self, response)`

This method is responsible for extracting the actual data from a detail page.

-   **Start with the common metadata**: The `item = self.extract_common_metadata(response)` line is already there.
-   **Identify selectors** for each data field you want to extract (e.g., title, description, authors).
-   **Use `response.css(...)` or `response.xpath(...)`** to extract the data.
-   **Use `.get()`** to get the first result, or **`.getall()`** to get a list of all results.
-   **Use `self.clean_text()`** to normalize extracted text.
-   **Update the `item` dictionary** with the extracted data.

**Example:**

```python
def parse_detail_page(self, response: Response) -> Dict[str, Any]:
    item = self.extract_common_metadata(response)

    item.update({
        'title': self.clean_text(response.css('h1.study-title::text').get()),
        'description': self.clean_text(' '.join(response.css('div.description *::text').getall())),
        'authors': response.css('ul.authors li::text').getall(),
        'publication_date': self.clean_text(response.css('span.date::text').get()),
    })

    return item
```

## Step 3: Configure Credentials (If Required)

If the platform requires authentication (`auth_required: true`):

1.  **Open `config/credentials.yaml`** (create it from the example if it doesn't exist).
2.  **Add an entry** for your new platform with the required credentials.

**Example:**

```yaml
my_new_platform:
  auth_method: "basic"
  username: "my_user"
  password: "my_secret_password"
```

## Step 4: Test the Spider

Before enabling the spider in production, test it locally.

Run the following command from the project root:

```bash
scrapy runspider spiders/my_new_platform_spider.py
```

-   Check the log output for any errors.
-   Verify that the spider is extracting data correctly.
-   A JSONL file should be created in `data/raw/my_new_platform/` with the scraped data.

## Step 5: Enable the Platform

Once you are confident that the spider is working correctly:

1.  **Open `config/platforms.yaml`**.
2.  **Find the entry** for your new platform.
3.  **Change `enabled: false` to `enabled: true`**.

## Step 6: Deploy

1.  **Commit your changes** to Git:

    ```bash
    git add spiders/my_new_platform_spider.py
    git add config/platforms.yaml
    git commit -m "feat: Add new platform adapter for MyNewPlatform"
    git push
    ```

2.  **Restart the Airflow services**: If you are running in Docker, you can restart the scheduler to pick up the new DAG.

    ```bash
    docker-compose restart airflow-scheduler
    ```

3.  **Verify in Airflow UI**: Open the Airflow UI (`http://localhost:8080`), and you should see a new DAG named `scrape_my_new_platform`. You can unpause it and trigger a manual run to verify.

That's it! You have successfully added a new platform to the scraping infrastructure.
