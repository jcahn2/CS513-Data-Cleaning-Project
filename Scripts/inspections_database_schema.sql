CREATE TABLE IF NOT EXISTS "businesses"(
"License #" TEXT, "Dt" TEXT, "DBA Name" TEXT, "AKA Name" TEXT,
 "Facility Type" TEXT, "Inspection Date" TEXT, "License # - Flag" TEXT);
CREATE TABLE IF NOT EXISTS "locations"(
"Location ID" TEXT, "Address" TEXT, "City" TEXT, "State" TEXT,
 "Zip" TEXT, "Latitude" TEXT, "Longitude" TEXT, "Location" TEXT);
CREATE TABLE IF NOT EXISTS "violations"(
"Violation ID" TEXT, "Inspection ID" TEXT, "Results" TEXT, "Violation Order" TEXT,
 "Violation Text" TEXT, "Violation Code" TEXT, "Violation Type" TEXT, "Violation Flag" TEXT);
CREATE TABLE IF NOT EXISTS "inspections"(
"License #" TEXT, "Inspection ID" TEXT, "Inspection Date" TEXT, "Inspection Type" TEXT,
 "Risk Category" TEXT, "Results" TEXT, "Location ID" TEXT);
