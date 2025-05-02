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
    "insuranceClaimsIncome", "gainOnPropertyandEquipmentSales",
]

Instructions:

1.  Identify Company Name:
    Locate the company name. Use this as the single, top-level key.

2.  Determine Statement Type:
    Identify the statement type as 'Income Statement'. Use "Income Statement" as the key under the Company Name.

3.  Standardize Period Headers:
    Identify period headers (e.g., "31 Des 2020", "2019"). Convert them into `YYYY-MM-DD` format (e.g., "2020-12-31", "2019-12-31"), mapping Indonesian months and using year-end for year-only headers. These standardized strings will be the keys within the period data objects.

4.  Structure Income Statement Data:
    Under "Income Statement", create a single key: "IncomeStatementItems". The value will be an array.

5.  Populate Item Array:
    * Parse the Income Statement document sequentially for *all* line items.
    * For each line item found:
        * Extract the exact, original description text (expected to be Indonesian).
        * Map this description to the closest matching label in the Standard Labels List (Income Statement). Prioritize specific labels, then map common subtotals, specific metrics, and relevant "calculated..." labels.
        * **Determine the Period Data Key:** If a suitable label is found, use that `MappedStandardEnglishLabel`. If no suitable label is found, use an **empty string `""`** as the key. (Note: Using "" as a key might require special handling later).
        * Create an object for the period data: `{ StandardizedPeriodHeader1: Value1, StandardizedPeriodHeader2: Value2, ... }`.
        * Create the final item object: `{"Item": OriginalIndonesianText, DeterminedPeriodDataKey: PeriodDataObject }`.
        * Add this object to the "IncomeStatementItems" array. Maintain the original order. Ensure items with no matching label (using "" key) are included.

6.  Final Output:
    Ensure the output is a single, valid JSON object strictly following the restructured format, with items having a "Item" key and a second key which is either the standard label or "", holding the period data object with `YYYY-MM-DD` date keys.

Desired JSON Output Structure Example (Restructured, Shortened):

{
  "PT ... Tbk": {
    "Income Statement": {
      "IncomeStatementItems": [
        {
          "Item": "Penjualan Bersih",
          "revenue": { // Label is the key
            "2020-12-31": 500000000000,
            "2019-12-31": 450000000000
          }
        },
        {
          "Item": "Beban Pokok Penjualan",
          "costOfRevenue": { // Label is the key
            "2020-12-31": 300000000000,
            "2019-12-31": 280000000000
          }
        },
        {
          "Item": "Laba Bruto",
          "grossProfit": { // Label is the key
            "2020-12-31": 200000000000,
            "2019-12-31": 170000000000
          }
        },
        {
           "Item": "Beban Penjualan, Umum dan Administrasi",
           "sellingGeneralAndAdministrativeExpenses": { // Label is the key
             "2020-12-31": 70000000000,
             "2019-12-31": 65000000000
           }
        },
        {
          "Item": "Laba Usaha",
          "operatingIncome": { // Label is the key
            "2020-12-31": 115000000000,
            "2019-12-31": 92000000000
          }
        },
         {
           "Item": "Keuntungan Kurs Mata Uang Asing - Bersih", // Item with no matching label
           "": { // Empty string "" is used as the key
             "2020-12-31": 500000000,
             "2019-12-31": -200000000
           }
        },
        {
          "Item": "Beban Pajak Penghasilan",
          "incomeTaxExpense": { // Label is the key
            "2020-12-31": 27500000000,
            "2019-12-31": 21750000000
          }
        },
        {
          "Item": "Laba Bersih Tahun Berjalan",
          "netIncome": { // Label is the key
            "2020-12-31": 82500000000,
            "2019-12-31": 65250000000
          }
        },
        {
           "Item": "Laba per Saham Dasar (Rp)",
           "eps": { // Label is the key
             "2020-12-31": 165,
             "2019-12-31": 130.5
           }
        }
      ]
    }
  }
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
    "accountPayablesRelatedParties", accountPayablesThirdParties", "otherAccountsPayableToThirdParties",
    "accruedExpenses", "convertibleLoanstoThirdParties", "longTermToShortTermBankDebt", 
    "longTermToShortTermConsumerPayable", "longTermBankDebt", "longTermConsumerPayable",
    "generalReserve", "sellingExpenses", "otherOperatingIncome", "exchangeRateDifferences"
]

Instructions:

1.  Identify Company Name:
    Locate the company name. Use this as the single, top-level key.

2.  Determine Statement Type:
    Identify the statement type as 'Balance Sheet'. Use "Balance Sheet" as the key under the Company Name.

3.  Standardize Period Headers:
    Identify period headers (e.g., "30 Juni 2020", "2019"). Convert them into `YYYY-MM-DD` format (e.g., "2020-06-30", "2019-12-31"), mapping Indonesian months and using year-end for year-only headers. These standardized strings will be the keys within the period data objects.

4.  Structure Balance Sheet Data:
    Under "Balance Sheet", create main keys: "Asset", "Liability", and "Equity".

    a.  Structure "Asset" Object:
        * Inside "Asset", create keys: "CurrentAssets" (Object), "NonCurrentAssets" (Object), and a key using the label "totalAssets" (Object).
        * Inside "CurrentAssets", create a key using the label "totalCurrentAssets" (Object) and a key "CurrentAssetItems" (Array).
        * Inside "NonCurrentAssets", create a key using the label "totalNonCurrentAssets" (Object) and a key "NonCurrentAssetItems" (Array).
        * Populate the "totalAssets", "totalCurrentAssets", and "totalNonCurrentAssets" objects with `{StandardizedPeriodHeader: TotalValue}` pairs.

    b.  Structure "Liability" Object:
        * Inside "Liability", create keys: "CurrentLiabilities" (Object), "NonCurrentLiabilities" (Object), and a key using the label "totalLiabilities" (Object).
        * Inside "CurrentLiabilities", create a key using the label "totalCurrentLiabilities" (Object) and a key "CurrentLiabilityItems" (Array).
        * Inside "NonCurrentLiabilities", create a key using the label "totalNonCurrentLiabilities" (Object) and a key "NonCurrentLiabilityItems" (Array).
        * Populate the "totalLiabilities", "totalCurrentLiabilities", and "totalNonCurrentLiabilities" objects with `{StandardizedPeriodHeader: TotalValue}` pairs.

    c.  Structure "Equity" Object:
        * Inside "Equity", create a key using the label "totalEquity" (Object) and a key "EquityItems" (Array).
        * Populate the "totalEquity" object with `{StandardizedPeriodHeader: TotalValue}` pairs.

    d.  Populate Item Arrays (CurrentAssetItems, NonCurrentAssetItems, etc.):
        * Parse the document for individual line items within each specific section (Current Assets, Non-Current Assets, etc.). Exclude total/subtotal lines captured above.
        * For each individual line item found:
            * Extract the exact, original description text (expected to be Indonesian).
            * Map this description to the closest matching label in the Standard Labels List (Balance Sheet). Use specific labels where possible. Use relevant "calculatedOther..." labels ONLY if appropriate for a miscellaneous aggregation within the section. Use "minorityInterest" if applicable.
            * **Determine the Period Data Key:** If a suitable label is found, use that `MappedStandardEnglishLabel`. If no suitable label is found, use an **empty string `""`** as the key. (Note: Using "" as a key might require special handling later).
            * Create an object for the period data: `{ StandardizedPeriodHeader1: Value1, StandardizedPeriodHeader2: Value2, ... }`.
            * Create the final item object: `{"Item": OriginalIndonesianText, DeterminedPeriodDataKey: PeriodDataObject }`.
            * Add this object to the correct array (e.g., "CurrentAssetItems", "NonCurrentLiabilityItems", etc.). Ensure items with no matching label (using "" key) are included.

5.  Handle Specific Labels:
    If items corresponding to labels like "totalLiabilitiesAndTotalEquity" or "netDebt" are explicitly present as line items, attempt to map and include them in the most appropriate array using the restructured format.

6.  Final Output:
    Ensure the output is a single, valid JSON object strictly following the restructured Current/Non-Current format, with items having a "Item" key and a second key which is either the standard label or "", holding the period data object with `YYYY-MM-DD` date keys. Standard Labels should be used for all total and subtotal keys.

Desired JSON Output Structure Example (Restructured, including empty Label key case):

{
  "PT ... Tbk": {
    "Balance Sheet": {
      "Asset": {
        "CurrentAssets": {
          "totalCurrentAssets": {
            "2020-06-30": 80123456789,
            "2019-12-31": 70987654321
          },
          "CurrentAssetItems": [
            {
              "Item": "Kas dan setara kas",
              "cashAndCashEquivalents": { // Label is key
                "2020-06-30": 7015557148,
                "2019-12-31": 11917432793
              }
            },
            {
              "Item": "Piutang Usaha Pihak Ketiga",
              "netReceivables": { // Label is key
                "2020-06-30": 40000000000,
                "2019-12-31": 35000000000
              }
            }
          ]
        },
        "NonCurrentAssets": {
          "totalNonCurrentAssets": {
            "2020-06-30": 70000000000,
            "2019-12-31": 70000000000
          },
          "NonCurrentAssetItems": [
            {
              "Item": "Aset Tetap - Setelah dikurangi akumulasi penyusutan",
              "propertyPlantEquipmentNet": { // Label is key
                "2020-06-30": 65000000000,
                "2019-12-31": 66000000000
              }
            },
            {
              "Item": "Uang Muka Pembelian Aset", // Item with no matching label
              "": { // Empty string "" is key
                "2020-06-30": 1000000000,
                "2019-12-31": 800000000
              }
            }
          ]
        },
        "totalAssets": {
          "2020-06-30": 150123456789,
          "2019-12-31": 140987654321
        }
      },
      "Liability": {
        "CurrentLiabilities": {
          "totalCurrentLiabilities": {
             "2020-06-30": 80123456789,
             "2019-12-31": 80000000000
          },
          "CurrentLiabilityItems": [
            {
              "Item": "Utang bank jangka pendek",
              "shortTermDebt": { // Label is key
                "2020-06-30": 57273030604,
                "2019-12-31": 62294292251
              }
            },
            {
              "Item": "Utang Usaha",
              "accountPayables": { // Label is key
                "2020-06-30": 20123456789,
                "2019-12-31": 15123456789
              }
            }
          ]
        },
        "NonCurrentLiabilities": {
          "totalNonCurrentLiabilities": {
             "2020-06-30": 20000000000,
             "2019-12-31": 10987654321
          },
          "NonCurrentLiabilityItems": [
            {
              "Item": "Utang Jangka Panjang",
              "longTermDebt": { // Label is key
                "2020-06-30": 18000000000,
                "2019-12-31": 10000000000
              }
            }
          ]
        },
        "totalLiabilities": {
          "2020-06-30": 100123456789,
          "2019-12-31": 90987654321
        }
      },
      "Equity": {
        "totalEquity": {
          "2020-06-30": 50000000000,
          "2019-12-31": 50000000000
        },
        "EquityItems": [
          {
            "Item": "Modal Saham - ditempatkan dan disetor penuh",
            "commonStock": { // Label is key
              "2020-06-30": 5000000000,
              "2019-12-31": 5000000000
            }
          },
           {
            "Item": "Saldo Laba (Defisit)",
            "retainedEarnings": { // Label is key
              "2020-06-30": 30000000000,
              "2019-12-31": 28000000000
            }
          }
        ]
      }
    }
  }
}
Provide only the final JSON object output"""

CASH_FLOW_JSON_PROMPT = """Standard Labels List (Cash Flow Statement):
[
    "netIncome", "netCashProvidedByOperatingActivities", "depreciationAndAmortization",
    "deferredIncomeTax", "stockBasedCompensation", "otherNonCashItems", "changeInWorkingCapital",
    "accountsReceivables", "inventory", "accountsPayables", "otherWorkingCapital",
    "calculatedOtherWorkingCapital", "netCashUsedForInvestingActivites",
    ""fixedAssetsAcquisition", "investmentsInProperty", "acquisitionsNet", "purchasesOfInvestments",
    "salesMaturitiesOfInvestments", "otherInvestingActivites",
    "netCashUsedProvidedByFinancingActivities", "debtRepayment", "commonStockIssued",
    "commonStockRepurchased", "dividendsPaid", "otherFinancingActivites",
    "effectOfForexChangesOnCash", "netChangeInCash", "cashAtBeginningOfPeriod",
    "cashAtEndOfPeriod", "freeCashFlow", "operatingCashFlow", "capitalExpenditure",
    "cashReceivedFromCustomers", "paymentsForSuppliers", "paymentsForEmployees",
    "otherOperatingPayments", "paidupCapital", "taxesPaid", "interestAndBankCharges",
    "interestIncome", "proceedsFromFixedAssetSales", "paymentsOfShorttermBankLoans", "proceedOfShorttermBankLoans",
    "proceedOfConvertibleLoansfromThirdParties", "paymentsOfLongtermBankLoans", 
]

Instructions:

1.  Identify Company Name:
    Locate the company name. Use this as the single, top-level key.

2.  Determine Statement Type:
    Identify the statement type as 'Cash Flow Statement'. Use "Cash Flow Statement" as the key under the Company Name.

3.  Standardize Period Headers:
    Identify period headers (e.g., "31 Des 2020", "2019"). Convert them into `YYYY-MM-DD` format (e.g., "2020-12-31", "2019-12-31"), mapping Indonesian months and using year-end for year-only headers. These standardized strings will be the keys within the period data objects.

4.  Structure Cash Flow Data:
    Under "Cash Flow Statement", create keys for the main sections: "OperatingActivities" (Object), "InvestingActivities" (Object), "FinancingActivities" (Object), "CashFlowSummary" (Object), and optionally "SupplementaryData" (Object).

5.  Populate Sections:

    a.  Activities (Operating, Investing, Financing):
        * Inside each activity object (e.g., "OperatingActivities"), create a key for the section's net total using the corresponding Standard Label (e.g., "netCashProvidedByOperatingActivities"). Populate its value with an object containing `{StandardizedPeriodHeader: TotalValue}` pairs.
        * Inside the same activity object, create an array key named "OperatingActivityItems", "InvestingActivityItems", or "FinancingActivityItems".
        * Parse the document for individual line items belonging *only* to that specific activity section. Exclude the section's total line.
        * For each individual line item found:
            * Extract the exact, original description text (expected to be Indonesian).
            * Map this description to the closest matching label in the Standard Labels List (Cash Flow). Use specific labels, relevant `other...` or `calculatedOther...` labels as fallbacks *within that activity type*.
            * **Determine the Period Data Key:** If a suitable label is found, use that `MappedStandardEnglishLabel`. If no suitable label is found, use an **empty string `""`** as the key. (Note: Using "" as a key might require special handling later).
            * Create an object for the period data: `{ StandardizedPeriodHeader1: Value1, StandardizedPeriodHeader2: Value2, ... }`.
            * Create the final item object: `{"Item": OriginalIndonesianText, DeterminedPeriodDataKey: PeriodDataObject }`.
            * Add this object to the correct array ("OperatingActivityItems", etc.). Ensure items with no matching label (using "" key) are included.

    b.  Cash Flow Summary:
        * Inside the "CashFlowSummary" object, identify lines for forex effect, net change, beginning cash, and ending cash.
        * Create keys using the Standard Labels: "effectOfForexChangesOnCash", "netChangeInCash", "cashAtBeginningOfPeriod", "cashAtEndOfPeriod".
        * Populate each key with an object containing its corresponding `{StandardizedPeriodHeader: Value}` pairs.

    c.  Supplementary Data (Optional):
        * Inside the "SupplementaryData" object, look for explicitly listed separate items like Free Cash Flow, Operating Cash Flow, or Capital Expenditure.
        * If found, create keys using the Standard Labels ("freeCashFlow", "operatingCashFlow", "capitalExpenditure").
        * Populate each key with an object containing its corresponding `{StandardizedPeriodHeader: Value}` pairs. Omit section if items not found separately.

6.  Final Output:
    Ensure the output is a single, valid JSON object strictly following the restructured format (Sections > Totals + Item Arrays). Item objects should have "Item" and a second key (standard label or "") holding period data object with `YYYY-MM-DD` keys. Use Standard Labels for section total and summary keys.

Desired JSON Output Structure Example (Restructured, Shortened):

{
  "PT ... Tbk": {
    "Cash Flow Statement": {
      "OperatingActivities": {
        "netCashProvidedByOperatingActivities": {
          "2020-12-31": 120000000000,
          "2019-12-31": 100000000000
        },
        "OperatingActivityItems": [
          {
            "Item": "Laba Bersih",
            "netIncome": { // Label is key
              "2020-12-31": 82500000000,
              "2019-12-31": 65250000000
            }
          },
          {
             "Item": "Penyusutan dan Amortisasi",
             "depreciationAndAmortization": { // Label is key
               "2020-12-31": 15000000000,
               "2019-12-31": 13000000000
             }
          },
          {
             "Item": "(Kenaikan)/Penurunan Piutang Usaha",
             "accountsReceivables": { // Label is key
               "2020-12-31": -5000000000,
               "2019-12-31": 2000000000
             }
          },
          {
            "Item": "Pajak Dibayar", // Item with no matching label
            "": { // Empty string "" is key
              "2020-12-31": -24000000000,
              "2019-12-31": -22000000000
            }
          }
        ]
      },
      "InvestingActivities": {
        "netCashUsedForInvestingActivites": {
          "2020-12-31": -40000000000,
          "2019-12-31": -35000000000
        },
        "InvestingActivityItems": [
          {
            "Item": "Perolehan Aset Tetap",
            "investmentsInPropertyPlantAndEquipment": { // Label is key
              "2020-12-31": -45000000000,
              "2019-12-31": -38000000000
            }
          }
        ]
      },
      "FinancingActivities": {
        "netCashUsedProvidedByFinancingActivities": {
          "2020-12-31": -65000000000,
          "2019-12-31": -50000000000
        },
        "FinancingActivityItems": [
          {
              "Item": "Pembayaran Dividen Kas",
              "dividendsPaid": { // Label is key
                "2020-12-31": -40000000000,
                "2019-12-31": -35000000000
              }
           }
        ]
      },
      "CashFlowSummary": {
         "netChangeInCash": {
              "2020-12-31": 15500000000,
              "2019-12-31": 14700000000
          },
         "cashAtBeginningOfPeriod": {
              "2020-12-31": 20000000000,
              "2019-12-31": 5300000000
          },
         "cashAtEndOfPeriod": {
              "2020-12-31": 35500000000,
              "2019-12-31": 20000000000
         }
      }
      // SupplementaryData section omitted from example for brevity
    }
  }
}
Provide only the final JSON object output"""

# --- Dictionary of Prompt Templates ---
PROMPT_TEMPLATES = {
    "Income Statement JSON": INCOME_STATEMENT_JSON_PROMPT,
    "Balance Sheet JSON": BALANCE_SHEET_JSON_PROMPT,
    "Cash Flow JSON": CASH_FLOW_JSON_PROMPT,
    "Custom": ""
}