#!/usr/bin/env python
"""Integration test for analytics endpoints."""
import httpx
import json

client = httpx.Client(base_url="http://127.0.0.1:8000")

print("=" * 70)
print("Testing Analytics Endpoints")
print("=" * 70 + "\n")

# First, seed some test data
employees_data = [
    {
        "emp_id": "ANA001",
        "full_name": "Alice Johnson",
        "email": "ana-alice@acme.com",
        "department": "Engineering",
        "country": "US",
        "job_title": "Senior Engineer",
        "band": "L4",
        "employment_type": "full-time",
        "status": "active",
        "base_salary": 150000.0,
        "currency": "USD",
    },
    {
        "emp_id": "ANA002",
        "full_name": "Bob Smith",
        "email": "ana-bob@acme.com",
        "department": "Engineering",
        "country": "US",
        "job_title": "Engineer",
        "band": "L3",
        "employment_type": "full-time",
        "status": "active",
        "base_salary": 120000.0,
        "currency": "USD",
    },
    {
        "emp_id": "ANA003",
        "full_name": "Carol Davis",
        "email": "ana-carol@acme.com",
        "department": "Sales",
        "country": "US",
        "job_title": "Sales Manager",
        "band": "L4",
        "employment_type": "full-time",
        "status": "active",
        "base_salary": 140000.0,
        "currency": "USD",
    },
    {
        "emp_id": "ANA004",
        "full_name": "Diana Brown",
        "email": "ana-diana@acme.com",
        "department": "Engineering",
        "country": "UK",
        "job_title": "Senior Engineer",
        "band": "L4",
        "employment_type": "full-time",
        "status": "active",
        "base_salary": 130000.0,
        "currency": "GBP",
    },
    {
        "emp_id": "ANA005",
        "full_name": "Eve Wilson",
        "email": "ana-eve@acme.com",
        "department": "Sales",
        "country": "UK",
        "job_title": "Contractor",
        "band": "L2",
        "employment_type": "contractor",
        "status": "active",
        "base_salary": 80000.0,
        "currency": "GBP",
    },
]

print("[Setup] Creating 5 test employees...")
for emp in employees_data:
    resp = client.post("/employees/", json=emp)
    assert resp.status_code == 201, f"Failed to create employee: {resp.status_code}"
print("✓ 5 employees created\n")

# Test 1: Salary Stats
print("[1] GET /analytics/salary-stats")
resp = client.get("/analytics/salary-stats")
assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
stats = resp.json()
print(f"    Overall: avg=${stats['overall']['avg']}, median=${stats['overall']['median']}, count={stats['overall']['count']}")
print(f"    By department: {len(stats['by_department'])} departments")
for dept in stats["by_department"]:
    print(f"      {dept['department']}: avg=${dept['avg']}, count={dept['count']}")
print(f"    By country: {len(stats['by_country'])} countries")
for country in stats["by_country"]:
    print(f"      {country['country']}: avg=${country['avg']}, count={country['count']}")
print()

# Test 2: Headcount
print("[2] GET /analytics/headcount")
resp = client.get("/analytics/headcount")
assert resp.status_code == 200
headcount = resp.json()
print(f"    Total active: {headcount['total']}")
print(f"    By department: {headcount['by_department']}")
print(f"    By country: {headcount['by_country']}")
print(f"    By employment type: {headcount['by_employment_type']}")
print()

# Test 3: Band Distribution
print("[3] GET /analytics/band-distribution")
resp = client.get("/analytics/band-distribution")
assert resp.status_code == 200
bands = resp.json()
print(f"    Total bands: {len(bands)}")
for band in bands:
    print(
        f"      {band['band']}: count={band['count']}, avg=${band['avg_salary']}, "
        f"min=${band['min_salary']}, max=${band['max_salary']}"
    )
print()

# Test 4: Top Earners (default limit=10)
print("[4] GET /analytics/top-earners")
resp = client.get("/analytics/top-earners")
assert resp.status_code == 200
top_earners = resp.json()
print(f"    Returned {len(top_earners)} top earners")
for i, emp in enumerate(top_earners, 1):
    print(f"      {i}. {emp['full_name']}: ${emp['base_salary']} ({emp['band']})")
print()

# Test 5: Top Earners with custom limit
print("[5] GET /analytics/top-earners?limit=2")
resp = client.get("/analytics/top-earners?limit=2")
assert resp.status_code == 200
top_2 = resp.json()
print(f"    Returned {len(top_2)} top earners")
assert len(top_2) <= 2, f"Expected at most 2, got {len(top_2)}"
for i, emp in enumerate(top_2, 1):
    print(f"      {i}. {emp['full_name']}: ${emp['base_salary']}")
print()

# Test 6: Verify limit constraints
print("[6] Testing limit constraints")
resp = client.get("/analytics/top-earners?limit=101")
assert resp.status_code == 422, "Expected 422 for limit > 100"
print("    ✓ limit=101 rejected (max=100)")
resp = client.get("/analytics/top-earners?limit=0")
assert resp.status_code == 422, "Expected 422 for limit < 1"
print("    ✓ limit=0 rejected (min=1)")
print()

print("=" * 70)
print("All analytics tests passed!")
print("=" * 70)
