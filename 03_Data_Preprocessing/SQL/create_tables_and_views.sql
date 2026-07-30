-- =========================================================================
-- SQL DDL & ANALYTICAL VIEWS FOR ASEAN CAPSTONE DATASET
-- Project: capstone-asean_overview_analysis
-- Database Compatibility: PostgreSQL / SQLite / SQL Server / MySQL
-- =========================================================================

-- -------------------------------------------------------------------------
-- 1. TABLE CREATION: Dim_Country
-- -------------------------------------------------------------------------
DROP TABLE IF EXISTS Dim_Country;
CREATE TABLE Dim_Country (
    CountryCode VARCHAR(3) PRIMARY KEY,
    CountryName VARCHAR(100) NOT NULL,
    SubRegion VARCHAR(50),
    Capital VARCHAR(100),
    ISO2 VARCHAR(2),
    Latitude DECIMAL(9,6),
    Longitude DECIMAL(9,6)
);

-- -------------------------------------------------------------------------
-- 2. TABLE CREATION: Dim_Indicator
-- -------------------------------------------------------------------------
DROP TABLE IF EXISTS Dim_Indicator;
CREATE TABLE Dim_Indicator (
    SeriesCode VARCHAR(50) PRIMARY KEY,
    SeriesName VARCHAR(255) NOT NULL,
    Domain VARCHAR(100),
    UnitOfMeasure VARCHAR(100)
);

-- -------------------------------------------------------------------------
-- 3. TABLE CREATION: Dim_Date
-- -------------------------------------------------------------------------
DROP TABLE IF EXISTS Dim_Date;
CREATE TABLE Dim_Date (
    Year INT PRIMARY KEY,
    Date DATE NOT NULL,
    YearLabel VARCHAR(20),
    Decade VARCHAR(20),
    Period VARCHAR(20)
);

-- -------------------------------------------------------------------------
-- 4. TABLE CREATION: Fact_ASEAN_Indicators
-- -------------------------------------------------------------------------
DROP TABLE IF EXISTS Fact_ASEAN_Indicators;
CREATE TABLE Fact_ASEAN_Indicators (
    CountryCode VARCHAR(3) NOT NULL,
    SeriesCode VARCHAR(50) NOT NULL,
    Year INT NOT NULL,
    Value DECIMAL(18,4),
    PRIMARY KEY (CountryCode, SeriesCode, Year),
    FOREIGN KEY (CountryCode) REFERENCES Dim_Country(CountryCode),
    FOREIGN KEY (SeriesCode) REFERENCES Dim_Indicator(SeriesCode),
    FOREIGN KEY (Year) REFERENCES Dim_Date(Year)
);

-- -------------------------------------------------------------------------
-- 5. TABLE CREATION: Fact_ASEAN_Tourism_Flow
-- -------------------------------------------------------------------------
DROP TABLE IF EXISTS Fact_ASEAN_Tourism_Flow;
CREATE TABLE Fact_ASEAN_Tourism_Flow (
    DestinationCountryCode VARCHAR(3) NOT NULL,
    OriginCountryCode VARCHAR(50) NOT NULL,
    Year INT NOT NULL,
    Visitors DECIMAL(18,4),
    PRIMARY KEY (DestinationCountryCode, OriginCountryCode, Year),
    FOREIGN KEY (DestinationCountryCode) REFERENCES Dim_Country(CountryCode),
    FOREIGN KEY (Year) REFERENCES Dim_Date(Year)
);


-- -------------------------------------------------------------------------
-- 6. ANALYTICAL VIEWS
-- -------------------------------------------------------------------------

-- View: ASEAN GDP Overview
CREATE VIEW vw_ASEAN_GDP_Overview AS
SELECT 
    c.CountryName,
    c.SubRegion,
    f.Year,
    f.Value AS GDP_Current_USD
FROM Fact_ASEAN_Indicators f
JOIN Dim_Country c ON f.CountryCode = c.CountryCode
WHERE f.SeriesCode = 'NY.GDP.MKTP.CD';

-- View: ASEAN Technology Adoption
CREATE VIEW vw_ASEAN_Tech_Adoption AS
SELECT 
    c.CountryName,
    f.Year,
    f.Value AS Internet_User_Pct
FROM Fact_ASEAN_Indicators f
JOIN Dim_Country c ON f.CountryCode = c.CountryCode
WHERE f.SeriesCode = 'IT.NET.USER.ZS';
