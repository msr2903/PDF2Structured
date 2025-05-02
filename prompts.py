INCOME_STATEMENT_JSON_PROMPT = """Standard Labels List (Income Statement):
[
    "revenue", "costOfRevenue", "grossProfit", "calculatedOperatingExpenses",
    "researchAndDevelopmentExpenses", "sellingGeneralAndAdministrativeExpenses",
    "calculatedOtherExpenses", "operatingIncome", "calculatedNetInterest",
    "interestIncome", "interestExpense", "calculatedOtherIncome", "incomeBeforeTax",
    "incomeTaxExpense", "calculatedIncomeNonControlling", "netIncome",
    "depreciationAndAmortization", "ebitda", "eps", "epsdiluted",
    "weightedAverageShsOut", "weightedAverageShsOutDil", "relatedTax",
    "otherComprehensiveIncome", "otherComprehensiveIncomeAfterTax", "totalComprehensiveIncome",
    "insuranceClaimsIncome", "gainOnPropertyandEquipmentSales"
]

Instructions:

1.  Identify Company Name:
    Locate the company name. Use this as the single, top-level key for the entire JSON output. The value associated with this key will be an array containing objects for "Income Statement", "Balance Sheet", "Cash Flow" etc.

2.  Determine Statement Type:
    Locate the 'Income Statement' section. Create an object `{"Income Statement": []}` within the top-level array mentioned in Step 1. The value associated with "Income Statement" will be an array where all the processed line items will be placed sequentially.

3.  Standardize Period Headers:
    Identify all period headers (e.g., "31 Des 2020", "2019", "Tahun yang berakhir 31 Desember 2020"). Convert them strictly into `YYYY-MM-DD` format (e.g., "2020-12-31", "2019-12-31"). Use year-end ('YYYY-12-31') for year-only headers. These standardized date strings are crucial for the 'date' key within the 'timeSeriesData' arrays.

4.  Structure Income Statement Data (Sequential Items):
    The value associated with the "Income Statement" key (created in Step 2) will be an array `[]`. This array will be populated directly with objects representing each line item from the source document, maintaining their original order.

5.  Populate Item Array:
    * Parse the Income Statement document sequentially for *all* line items presented.
    * For each line item found:
        * Extract the exact, original description text (expected to be Indonesian). Use this text as the value for the `id` key in the item object.
        * Map this description to the closest matching label in the Standard Labels List (Income Statement). Use the mapped English label as the value for the `label` key. Prioritize specific labels (e.g., "revenue", "netIncome") over broader ones. If no suitable standard label is found, use an **empty string `""`** as the value for the `label` key.
        * Extract the financial figures for each standardized period header. Format these figures into an array assigned to the `timeSeriesData` key, like: `[{"date": "YYYY-MM-DD", "figure": Value1}, {"date": "YYYY-MM-DD", "figure": Value2}, ...]`. Ensure values are captured as numbers.
        * Create the final item object using the extracted information: `{"id": OriginalIndonesianText, "label": MappedStandardEnglishLabelOrEmptyString, "timeSeriesData": PeriodDataObjectArray }`.
        * Append this item object directly to the array associated with the "Income Statement" key. Maintain the original order of items as presented in the source document.
        * **Note:** Individual Income Statement line items usually do *not* have nested children. Do not add a `children` key to these item objects unless the source document explicitly shows sub-items indented under a specific line item.

6.  Final Output Structure:
    Ensure the final output is a single JSON object starting with the Company Name key. Inside, the "Income Statement" key should hold an array containing objects for each line item. Each item object must strictly follow the structure using `id` (original Indonesian text), `label` (mapped English label or ""), and `timeSeriesData` (array of `{"date": "YYYY-MM-DD", "figure": Value}`) as demonstrated in the example below.

Desired JSON Output Structure Example (Hierarchical Items):

{
  "PT ... Tbk": [ // Array value for Company Name Key
    {"Income Statement": [ // Array value for Income Statement Key, holding item objects directly
      {
        "id": "Penjualan Bersih", // Original Text
        "label": "revenue",      // Mapped Label
        "timeSeriesData": [
          {"date": "2020-12-31", "figure": 500000000000},
          {"date": "2019-12-31", "figure": 450000000000}
        ]
      },
      {
        "id": "Beban Pokok Penjualan",
        "label": "costOfRevenue",
        "timeSeriesData": [
          {"date": "2020-12-31", "figure": 300000000000},
          {"date": "2019-12-31", "figure": 280000000000}
        ]
      },
      {
        "id": "Laba Bruto",
        "label": "grossProfit",
        "timeSeriesData": [
          {"date": "2020-12-31", "figure": 200000000000},
          {"date": "2019-12-31", "figure": 170000000000}
        ]
      },
      {
        "id": "Beban Penjualan, Umum dan Administrasi",
        "label": "sellingGeneralAndAdministrativeExpenses",
        "timeSeriesData": [
          {"date": "2020-12-31", "figure": 70000000000},
          {"date": "2019-12-31", "figure": 65000000000}
        ]
      },
      {
        "id": "Laba Usaha",
        "label": "operatingIncome",
        "timeSeriesData": [
          {"date": "2020-12-31", "figure": 115000000000},
          {"date": "2019-12-31", "figure": 92000000000}
        ]
      },
      {
        "id": "Keuntungan Kurs Mata Uang Asing - Bersih", // Item with no matching label example
        "label": "", // Empty string label
        "timeSeriesData": [
          {"date": "2020-12-31", "figure": 500000000},
          {"date": "2019-12-31", "figure": -200000000} // Handle negative values appropriately
        ]
      },
      {
        "id": "Beban Pajak Penghasilan",
        "label": "incomeTaxExpense",
        "timeSeriesData": [
          {"date": "2020-12-31", "figure": 27500000000},
          {"date": "2019-12-31", "figure": 21750000000}
        ]
      },
      {
        "id": "Laba Bersih Tahun Berjalan",
        "label": "netIncome",
        "timeSeriesData": [
          {"date": "2020-12-31", "figure": 82500000000},
          {"date": "2019-12-31", "figure": 65250000000}
        ]
      },
      {
        "id": "Laba per Saham Dasar (Rp)",
        "label": "eps",
        "timeSeriesData": [
          {"date": "2020-12-31", "figure": 165}, // EPS values are often smaller units
          {"date": "2019-12-31", "figure": 130.5}
        ]
      }
      // ... other income statement items ...
    ]},
    {"Balance Sheet": []}, // Placeholder
    {"Cash Flow": []}      // Placeholder
  ]
}
Provide only the final JSON output"""

BALANCE_SHEET_JSON_PROMPT = """Standard Labels List (Balance Sheet):
[
    "totalCurrentAssets", "cashAndShortTermInvestments", "cashAndCashEquivalents",
    "shortTermInvestments", "netReceivables", "inventory", "calculatedOtherCurrentAssets",
    "totalAssets", "totalNonCurrentAssets", "propertyPlantEquipmentNet",
    "goodwillAndIntangibleAssets", "goodwill", "intangibleAssets", "longTermInvestments",
    "taxAssets", "calculatedOtherNonCurrentAssets", "totalCurrentLiabilities",
    "accountPayables", "shortTermDebt", "taxPayables", "deferredRevenue",
    "calculatedOtherCurrentLiabilities", "totalLiabilities", "totalNonCurrentLiabilities",
    "longTermDebt", "deferredTaxLiabilitiesNonCurrent", "deferredRevenueNonCurrent",
    "capitalLeaseObligations", "calculatedOtherNonCurrentLiabilities", "totalEquity",
    "minorityInterest", "totalStockholdersEquity", "retainedEarnings",
    "accumulatedOtherComprehensiveIncomeLoss", "commonStock", "preferredStock",
    "othertotalStockholdersEquity", "totalLiabilitiesAndTotalEquity",
    "totalLiabilitiesAndStockholdersEquity", "totalInvestments", "totalDebt", "netDebt",
    "prepaidExpenses", "Advances", "prepaidTax", "claimsForTaxRefund",
    "accountPayablesRelatedParties", "accountPayablesThirdParties", "otherAccountsPayableToThirdParties",
    "accruedExpenses", "convertibleLoanstoThirdParties", "longTermToShortTermBankDebt",
    "longTermToShortTermConsumerPayable", "longTermBankDebt", "longTermConsumerPayable",
    "generalReserve", "sellingExpenses", "otherOperatingIncome", "exchangeRateDifferences",
    // Add core hierarchy labels if needed for mapping totals/subtotals explicitly, though instructions focus on position:
    "asset", "currentAsset", "nonCurrentAsset", "liability", "currentLiability", "nonCurrentLiability", "equity"
]

Instructions:

1.  Identify Company Name:
    Locate the company name. Use this as the single, top-level key for the entire JSON output. The value associated with this key will be an array containing objects for "Income Statement", "Balance Sheet", "Cash Flow" etc.

2.  Determine Statement Type:
    Locate the 'Balance Sheet' section. Create an object `{"Balance Sheet": []}` within the top-level array mentioned in Step 1. The value associated with "Balance Sheet" will be an array where the main financial categories (Asset, Liability, Equity) are placed.

3.  Standardize Period Headers:
    Identify all period headers (e.g., "30 Juni 2020", "2019"). Convert them strictly into `YYYY-MM-DD` format (e.g., "2020-06-30", "2019-12-31"). Use year-end ('YYYY-12-31') for year-only headers. These standardized date strings are crucial for the 'date' key within the 'timeSeriesData' arrays.

4.  Structure Balance Sheet Data (Hierarchical):
    Populate the array associated with the "Balance Sheet" key by creating objects for the main financial categories:

    a.  **Asset Object:**
        * Create an object for Assets.
        * Set its `id` to the original Indonesian term found (e.g., "Aset").
        * Set its `label` to "asset".
        * Find the corresponding total asset value line. Extract the figures for each period and format them into an array like `[{"date": "YYYY-MM-DD", "figure": Value1}, {"date": "YYYY-MM-DD", "figure": Value2}, ...]`. Assign this array to the `timeSeriesData` key for this Asset object.
        * Create a `children` key with an empty array `[]` as its value.

    b.  **Asset Children (Current/Non-Current):**
        * **Current Assets Node:** Identify the Current Assets section under Assets. Create an object for it. Set `id` to its Indonesian name (e.g., "Aset Lancar"), `label` to "currentAsset". Find its subtotal value line, extract figures, and format into its `timeSeriesData` array. Create a `children` array `[]` for its line items. Add this Current Assets object to the `children` array of the main Asset object (from 4a).
        * **Current Asset Items:** For each individual line item *under* Current Assets (excluding the subtotal line):
            * Extract the exact original Indonesian text. Use this as the `id` for the item object.
            * Map the Indonesian text to the closest Standard Label List entry. Use the English label as the `label`. If no match, use `""` (empty string) for the `label`.
            * Extract the figures for each period and format into the `timeSeriesData` array `[{"date": "YYYY-MM-DD", "figure": Value1}, ...]`.
            * Create the final item object: `{"id": ..., "label": ..., "timeSeriesData": [...]}`.
            * Add this item object to the `children` array of the Current Assets node created above. These item objects typically do *not* have their own `children` key.
        * **Non-Current Assets Node:** Identify the Non-Current Assets section. Create an object similarly: `id` (e.g., "Aset Tidak Lancar"), `label` ("nonCurrentAsset"), `timeSeriesData` (from its subtotal line), and an empty `children` array `[]`. Add this Non-Current Assets object to the `children` array of the main Asset object (from 4a).
        * **Non-Current Asset Items:** Process individual line items under Non-Current Assets using the same method as Current Asset Items, adding the resulting objects `{"id": ..., "label": ..., "timeSeriesData": [...]}` to the `children` array of the Non-Current Assets node.

    c.  **Liability Object and Children:**
        * Create the main Liability object: `id` (e.g., "Liabilitas"), `label` ("liability"), `timeSeriesData` (from total liability line). Add an empty `children` array. Add this object to the main "Balance Sheet" array (alongside the Asset object).
        * Create Current Liability node: `id` (e.g., "Liabilitas Jangka Pendek"), `label` ("currentLiability"), `timeSeriesData` (from subtotal), empty `children` array. Add this to the main Liability object's `children`.
        * Process Current Liability items and add them to the Current Liability node's `children`.
        * Create Non-Current Liability node: `id` (e.g., "Liabilitas Jangka Panjang"), `label` ("nonCurrentLiability"), `timeSeriesData` (from subtotal), empty `children` array. Add this to the main Liability object's `children`.
        * Process Non-Current Liability items and add them to the Non-Current Liability node's `children`.

    d.  **Equity Object and Children:**
        * Create the main Equity object: `id` (e.g., "Ekuitas"), `label` ("equity"), `timeSeriesData` (from total equity line). Add an empty `children` array. Add this object to the main "Balance Sheet" array.
        * Process individual line items under Equity (excluding the total line) using the same item processing method (id, label mapping, timeSeriesData) and add the resulting objects to the `children` array of the main Equity object.

5.  Handle Specific Labels (as Items):
    If items like "Kepentingan Nonpengendali" (minorityInterest) or others from the Standard Labels List appear as distinct line items *within* a section (Asset, Liability, Equity children), process them according to the item processing rules in Step 4 (id, label mapping, timeSeriesData) and place them in the appropriate `children` array. Do not confuse these with the main Total/Subtotal lines captured in the `timeSeriesData` of the parent nodes.

6.  Final Output Structure:
    Ensure the final output is a single JSON object starting with the Company Name. Inside, the "Balance Sheet" key should hold an array containing the main Asset, Liability, and Equity objects. These objects and their nested children must strictly follow the hierarchical structure using `id` (original Indonesian text), `label` (mapped English label or ""), `timeSeriesData` (array of `{"date": "YYYY-MM-DD", "figure": Value}`), and `children` (array for nested items/categories) as demonstrated in the example below.

Desired JSON Output Structure Example (Hierarchical):

{
  "PT Companyname": [ // Array value for Company Name Key
    {"Income Statement": []}, // Placeholder
    {"Balance Sheet": [ // Array value for Balance Sheet Key
      { // Asset Object
        "id": "Aset",
        "label": "asset",
        "timeSeriesData": [
          {"date": "2020-06-30", "figure": 276235766149}, // Example Total Value
          {"date": "2019-12-31", "figure": 250123456789}  // Example Total Value
        ],
        "children": [
          { // Current Asset Node
            "id": "Aset Lancar",
            "label": "currentAsset",
            "timeSeriesData": [
              {"date": "2020-06-30", "figure": 80123456789}, // Example Subtotal Value
              {"date": "2019-12-31", "figure": 70987654321}  // Example Subtotal Value
            ],
            "children": [
              { // Current Asset Item 1
                "id": "Kas dan setara kas",
                "label": "cashAndCashEquivalents", // Mapped Label
                "timeSeriesData": [
                  {"date": "2020-06-30", "figure": 7015557148},
                  {"date": "2019-12-31", "figure": 11917432793}
                ]
                // No 'children' key for typical items
              },
              { // Current Asset Item 2
                "id": "Piutang Usaha Pihak Ketiga",
                "label": "netReceivables", // Mapped Label (assuming this maps best)
                "timeSeriesData": [
                   {"date": "2020-06-30", "figure": 40000000000},
                   {"date": "2019-12-31", "figure": 35000000000}
                ]
              },
              { // Current Asset Item 3 - Unmapped Example
                "id": "Pajak Dibayar Dimuka",
                "label": "", // Empty string label - No direct match or decided not to map
                "timeSeriesData": [
                   {"date": "2020-06-30", "figure": 123456789},
                   {"date": "2019-12-31", "figure": 98765432}
                ]
              }
              // ... more current asset items
            ]
          },
          { // Non-Current Asset Node
            "id": "Aset Tidak Lancar",
            "label": "nonCurrentAsset",
            "timeSeriesData": [
              {"date": "2020-06-30", "figure": 196112309360}, // Example Subtotal Value
              {"date": "2019-12-31", "figure": 179135802468}  // Example Subtotal Value
            ],
            "children": [
              { // Non-Current Asset Item 1
                "id": "Aset Tetap - Setelah dikurangi akumulasi penyusutan",
                "label": "propertyPlantEquipmentNet", // Mapped Label
                "timeSeriesData": [
                  {"date": "2020-06-30", "figure": 65000000000},
                  {"date": "2019-12-31", "figure": 66000000000}
                ]
              }
              // ... more non-current asset items
            ]
          }
        ]
      },
      { // Liability Object (Structure mirrors Asset)
        "id": "Liabilitas",
        "label": "liability",
        "timeSeriesData": [ /* Total Liability figures */ ],
        "children": [
          { // Current Liability Node
            "id": "Liabilitas Jangka Pendek",
            "label": "currentLiability",
            "timeSeriesData": [ /* Subtotal Current Liability figures */ ],
            "children": [ /* Processed Current Liability line items */ ]
          },
          { // Non-Current Liability Node
            "id": "Liabilitas Jangka Panjang",
            "label": "nonCurrentLiability",
            "timeSeriesData": [ /* Subtotal Non-Current Liability figures */ ],
            "children": [ /* Processed Non-Current Liability line items */ ]
          }
        ]
      },
      { // Equity Object
        "id": "Ekuitas",
        "label": "equity",
        "timeSeriesData": [ /* Total Equity figures */ ],
        "children": [ /* Processed Equity line items */ ]
      }
    ]},
    {"Cash Flow": []} // Placeholder
  ]
}
Provide only the final JSON object output"""

CASH_FLOW_JSON_PROMPT = """Standard Labels List (Cash Flow Statement):
[
    "netIncome", "netCashProvidedByOperatingActivities", "depreciationAndAmortization",
    "deferredIncomeTax", "stockBasedCompensation", "otherNonCashItems", "changeInWorkingCapital",
    "accountsReceivables", "inventory", "accountsPayables", "otherWorkingCapital",
    "calculatedOtherWorkingCapital", "netCashUsedForInvestingActivites", // Note: Typo in original list? "Activities"
    "fixedAssetsAcquisition", "investmentsInPropertyPlantAndEquipment", // Added common variant
    "acquisitionsNet", "purchasesOfInvestments",
    "salesMaturitiesOfInvestments", "otherInvestingActivites", // Note: Typo in original list? "Activities"
    "netCashUsedProvidedByFinancingActivities", "debtRepayment", "commonStockIssued",
    "commonStockRepurchased", "dividendsPaid", "otherFinancingActivites", // Note: Typo in original list? "Activities"
    "effectOfForexChangesOnCash", "netChangeInCash", "cashAtBeginningOfPeriod",
    "cashAtEndOfPeriod", "freeCashFlow", "operatingCashFlow", "capitalExpenditure",
    "cashReceivedFromCustomers", "paymentsForSuppliers", "paymentsForEmployees",
    "otherOperatingPayments", "paidupCapital", "taxesPaid", "interestAndBankCharges",
    "interestIncome", "proceedsFromFixedAssetSales", "paymentsOfShorttermBankLoans", "proceedOfShorttermBankLoans",
    "proceedOfConvertibleLoansfromThirdParties", "paymentsOfLongtermBankLoans",
    // Add core hierarchy labels if needed for mapping section nodes:
    "operatingActivities", "investingActivities", "financingActivities", "cashFlowSummary", "supplementaryData"
]

Instructions:

1.  Identify Company Name:
    Locate the company name. Use this as the single, top-level key for the entire JSON output. The value associated with this key will be an array containing objects for "Income Statement", "Balance Sheet", "Cash Flow Statement" etc.

2.  Determine Statement Type:
    Locate the 'Cash Flow Statement' section. Create an object `{"Cash Flow Statement": []}` within the top-level array mentioned in Step 1. The value associated with "Cash Flow Statement" will be an array where the main section nodes (Operating, Investing, Financing, Summary) will be placed.

3.  Standardize Period Headers:
    Identify all period headers (e.g., "31 Des 2020", "2019"). Convert them strictly into `YYYY-MM-DD` format (e.g., "2020-12-31", "2019-12-31"). Use year-end ('YYYY-12-31') for year-only headers. These standardized date strings are crucial for the 'date' key within the 'timeSeriesData' arrays.

4.  Structure Cash Flow Data (Hierarchical Sections):
    Populate the array associated with the "Cash Flow Statement" key by creating objects (nodes) for the main sections:

    a.  **Operating Activities Node:**
        * Identify the Operating Activities section header (e.g., "Arus Kas dari Aktivitas Operasi"). Use this as the `id`.
        * Set the `label` for this node to "operatingActivities".
        * Find the line showing the *net total cash flow* for this section (e.g., "Kas bersih yang diperoleh dari aktivitas operasi"). Map its description to the corresponding Standard Label (e.g., "netCashProvidedByOperatingActivities"). Extract the figures for each period and format them into an array like `[{"date": "YYYY-MM-DD", "figure": Value1}, ...]`. Assign this array to the `timeSeriesData` key for this Operating Activities node.
        * Create a `children` key with an empty array `[]` as its value. This array will hold the individual line items for this section.
        * Add this completed Operating Activities node object to the main array under the "Cash Flow Statement" key.

    b.  **Operating Activity Items:**
        * Parse the individual line items listed *within* the Operating Activities section (e.g., net income, depreciation, changes in working capital items). Exclude the section's total line already captured in 4a.
        * For each individual line item found:
            * Extract the exact original Indonesian text. Use this as the `id` for the item object.
            * Map this description to the closest matching label in the Standard Labels List. Use the English label as the `label`. If no match, use `""` (empty string) for the `label`.
            * Extract the figures for each period and format into the `timeSeriesData` array `[{"date": "YYYY-MM-DD", "figure": Value1}, ...]`.
            * Create the final item object: `{"id": ..., "label": ..., "timeSeriesData": [...]}`.
            * Add this item object to the `children` array of the Operating Activities node created in step 4a.

    c.  **Investing Activities Node and Items:**
        * Repeat step 4a for the Investing Activities section: Create a node with `id` (e.g., "Arus Kas dari Aktivitas Investasi"), `label` ("investingActivities"), and `timeSeriesData` (containing the *net total* figures for investing activities, mapped to e.g., "netCashUsedForInvestingActivites"). Add an empty `children` array. Add this node to the main "Cash Flow Statement" array.
        * Repeat step 4b for the items *within* the Investing Activities section, adding the processed item objects `{"id": ..., "label": ..., "timeSeriesData": [...]}` to this node's `children` array.

    d.  **Financing Activities Node and Items:**
        * Repeat step 4a for the Financing Activities section: Create a node with `id` (e.g., "Arus Kas dari Aktivitas Pendanaan"), `label` ("financingActivities"), and `timeSeriesData` (containing the *net total* figures for financing activities, mapped to e.g., "netCashUsedProvidedByFinancingActivities"). Add an empty `children` array. Add this node to the main "Cash Flow Statement" array.
        * Repeat step 4b for the items *within* the Financing Activities section, adding the processed item objects `{"id": ..., "label": ..., "timeSeriesData": [...]}` to this node's `children` array.

    e.  **Cash Flow Summary Node and Items:**
        * Identify the summary section usually found at the end (showing net change, beginning/ending cash). Create a node object for this section. Set `id` to its header (e.g., "Ringkasan Arus Kas" or similar, adjust if headers differ), set `label` to "cashFlowSummary". This node typically does *not* represent a single total value, so it may not need a `timeSeriesData` key itself (or it could hold the 'netChangeInCash' figures if appropriate). Initialize an empty `children` array `[]`. Add this node to the main "Cash Flow Statement" array.
        * Process the individual line items *within* this summary section (e.g., Effect of Forex, Net Change in Cash, Cash at Beginning, Cash at End). Apply the item processing logic from step 4b: create objects `{"id": ..., "label": ..., "timeSeriesData": [...]}` using appropriate Standard Labels ("effectOfForexChangesOnCash", "netChangeInCash", "cashAtBeginningOfPeriod", "cashAtEndOfPeriod") for the `label` key. Add these summary item objects to the `children` array of the Cash Flow Summary node.

    f.  **Supplementary Data (Optional):**
        * Check if items like Free Cash Flow, Operating Cash Flow, or Capital Expenditure are listed separately, often after the main statement or in notes.
        * If found and desired, they could either be added as items to the `children` of the "cashFlowSummary" node (using labels "freeCashFlow", etc.) or potentially grouped under a dedicated "Supplementary Data" node (`id`: "Data Tambahan", `label`: "supplementaryData") which would itself contain these items in its `children` array. Choose the approach that best represents the source document layout.

5.  Final Output Structure:
    Ensure the final output is a single JSON object starting with the Company Name. Inside, the "Cash Flow Statement" key should hold an array containing the main section node objects (Operating, Investing, Financing, Summary). Each section node must follow the structure `id` (original header), `label` (section type), `timeSeriesData` (representing the section's net total, array of `{"date": ..., "figure": ...}`), and `children` (array holding item objects). Each item object within the `children` arrays must use the structure `id` (original text), `label` (mapped English label or ""), and `timeSeriesData` (array of `{"date": ..., "figure": ...}`).

Desired JSON Output Structure Example (Hierarchical Sections and Items):

{
  "PT ... Tbk": [ // Array value for Company Name Key
    {"Income Statement": []}, // Placeholder
    {"Balance Sheet": []},    // Placeholder
    {"Cash Flow Statement": [ // Array value for Cash Flow Key, holding section node objects
      { // Operating Activities Node
        "id": "Arus Kas dari Aktivitas Operasi",
        "label": "operatingActivities",
        "timeSeriesData": [ // Represents Net Cash from Operating Activities
          {"date": "2020-12-31", "figure": 120000000000},
          {"date": "2019-12-31", "figure": 100000000000}
        ],
        "children": [
          { // Operating Item 1
            "id": "Laba Bersih Sebelum Pajak", // Example ID, adjust based on source
            "label": "incomeBeforeTax", // Map appropriately
            "timeSeriesData": [
               {"date": "2020-12-31", "figure": 110000000000}, // Example value
               {"date": "2019-12-31", "figure": 87000000000}
            ]
          },
          { // Operating Item 2
             "id": "Penyusutan dan Amortisasi",
             "label": "depreciationAndAmortization",
             "timeSeriesData": [
                {"date": "2020-12-31", "figure": 15000000000},
                {"date": "2019-12-31", "figure": 13000000000}
             ]
          },
          { // Operating Item 3
             "id": "(Kenaikan)/Penurunan Piutang Usaha",
             "label": "accountsReceivables", // Label reflects the change in this account
             "timeSeriesData": [
                {"date": "2020-12-31", "figure": -5000000000},
                {"date": "2019-12-31", "figure": 2000000000}
             ]
           },
           { // Operating Item 4 - Unmapped Example
             "id": "Pajak Penghasilan Dibayar",
             "label": "", // Or potentially map to "taxesPaid" if available/appropriate
             "timeSeriesData": [
                 {"date": "2020-12-31", "figure": -24000000000},
                 {"date": "2019-12-31", "figure": -22000000000}
             ]
           }
          // ... other operating activity items
        ]
      },
      { // Investing Activities Node
        "id": "Arus Kas dari Aktivitas Investasi",
        "label": "investingActivities",
        "timeSeriesData": [ // Represents Net Cash used for Investing Activities
          {"date": "2020-12-31", "figure": -40000000000},
          {"date": "2019-12-31", "figure": -35000000000}
        ],
        "children": [
          { // Investing Item 1
            "id": "Perolehan Aset Tetap",
            "label": "investmentsInPropertyPlantAndEquipment", // Or fixedAssetsAcquisition
            "timeSeriesData": [
              {"date": "2020-12-31", "figure": -45000000000},
              {"date": "2019-12-31", "figure": -38000000000}
            ]
          },
          { // Investing Item 2
             "id": "Hasil Penjualan Aset Tetap",
             "label": "proceedsFromFixedAssetSales",
             "timeSeriesData": [
                 {"date": "2020-12-31", "figure": 5000000000},
                 {"date": "2019-12-31", "figure": 3000000000}
             ]
          }
          // ... other investing activity items
        ]
      },
      { // Financing Activities Node
        "id": "Arus Kas dari Aktivitas Pendanaan",
        "label": "financingActivities",
        "timeSeriesData": [ // Represents Net Cash used/provided by Financing Activities
          {"date": "2020-12-31", "figure": -65000000000},
          {"date": "2019-12-31", "figure": -50000000000}
        ],
        "children": [
          { // Financing Item 1
            "id": "Pembayaran Dividen Kas",
            "label": "dividendsPaid",
            "timeSeriesData": [
              {"date": "2020-12-31", "figure": -40000000000},
              {"date": "2019-12-31", "figure": -35000000000}
            ]
          },
          { // Financing Item 2
            "id": "Penerimaan Pinjaman Bank Jangka Pendek",
            "label": "proceedOfShorttermBankLoans",
            "timeSeriesData": [
                {"date": "2020-12-31", "figure": 10000000000},
                {"date": "2019-12-31", "figure": 5000000000}
            ]
          },
          { // Financing Item 3
            "id": "Pembayaran Pinjaman Bank Jangka Pendek",
            "label": "paymentsOfShorttermBankLoans",
            "timeSeriesData": [
                {"date": "2020-12-31", "figure": -35000000000},
                {"date": "2019-12-31", "figure": -20000000000}
            ]
          }
          // ... other financing activity items
        ]
      },
      { // Cash Flow Summary Node
        "id": "Ringkasan Arus Kas", // Example ID
        "label": "cashFlowSummary",
        // "timeSeriesData": [...] // Optional: Could hold netChangeInCash figures here instead of as a child item
        "children": [
          { // Summary Item 1
            "id": "Pengaruh Perubahan Kurs Mata Uang Asing",
            "label": "effectOfForexChangesOnCash",
            "timeSeriesData": [
                {"date": "2020-12-31", "figure": 500000000}, // Example
                {"date": "2019-12-31", "figure": -300000000}
            ]
          },
          { // Summary Item 2
            "id": "Kenaikan (Penurunan) Bersih Kas dan Setara Kas",
            "label": "netChangeInCash",
            "timeSeriesData": [
              {"date": "2020-12-31", "figure": 15500000000},
              {"date": "2019-12-31", "figure": 14700000000}
            ]
          },
          { // Summary Item 3
            "id": "Kas dan Setara Kas Awal Tahun",
            "label": "cashAtBeginningOfPeriod",
            "timeSeriesData": [
              {"date": "2020-12-31", "figure": 20000000000},
              {"date": "2019-12-31", "figure": 5300000000}
            ]
          },
          { // Summary Item 4
            "id": "Kas dan Setara Kas Akhir Tahun",
            "label": "cashAtEndOfPeriod",
            "timeSeriesData": [
              {"date": "2020-12-31", "figure": 35500000000},
              {"date": "2019-12-31", "figure": 20000000000}
            ]
          }
          // Optional: Add supplementary items like FCF here if found
        ]
      }
    ]}
  ]
}
Provide only the final JSON object output"""

# --- Dictionary of Prompt Templates ---
PROMPT_TEMPLATES = {
    "Income Statement JSON": INCOME_STATEMENT_JSON_PROMPT,
    "Balance Sheet JSON": BALANCE_SHEET_JSON_PROMPT,
    "Cash Flow JSON": CASH_FLOW_JSON_PROMPT,
    "Custom": ""
}