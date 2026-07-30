// =========================================================================
// POWER QUERY M-CODE SCRIPT FOR POWER BI DATA IMPORT (REFACTORED)
// Project: capstone-asean_overview_analysis
// Architecture: Star Schema (Fact + Fact Flow + Dimensions)
// =========================================================================

// -------------------------------------------------------------------------
// 1. QUERY: Dim_Country
// -------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\kelangthanghocIT\UTH\capstone-asean_overview_analysis\02_Data\Cleaned\Dim_Country.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"CountryCode", type text},
        {"CountryName", type text},
        {"SubRegion", type text},
        {"Capital", type text},
        {"ISO2", type text},
        {"Latitude", type number},
        {"Longitude", type number}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------
// 2. QUERY: Dim_Indicator
// -------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\kelangthanghocIT\UTH\capstone-asean_overview_analysis\02_Data\Cleaned\Dim_Indicator.csv"),[Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"SeriesCode", type text},
        {"SeriesName", type text},
        {"Domain", type text},
        {"UnitOfMeasure", type text}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------
// 3. QUERY: Dim_Date (Power BI Time Intelligence Supported)
// -------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\kelangthanghocIT\UTH\capstone-asean_overview_analysis\02_Data\Cleaned\Dim_Date.csv"),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Year", Int64.Type},
        {"Date", type date},
        {"YearLabel", type text},
        {"Decade", type text},
        {"Period", type text}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------
// 4. QUERY: Fact_ASEAN_Indicators
// -------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\kelangthanghocIT\UTH\capstone-asean_overview_analysis\02_Data\Cleaned\Fact_ASEAN_Indicators.csv"),[Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"CountryCode", type text},
        {"SeriesCode", type text},
        {"Year", Int64.Type},
        {"Value", type number}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------
// 5. QUERY: Fact_ASEAN_Tourism_Flow (Matrix Origin-Destination Analysis)
// -------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\kelangthanghocIT\UTH\capstone-asean_overview_analysis\02_Data\Cleaned\Fact_ASEAN_Tourism_Flow.csv"),[Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"DestinationCountryCode", type text},
        {"OriginCountryCode", type text},
        {"Year", Int64.Type},
        {"Visitors", type number}
    })
in
    #"Changed Type"
