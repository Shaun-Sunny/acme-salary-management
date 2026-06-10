#!/usr/bin/env python
"""Quick integration test for employee CRUD endpoints."""
import httpx

client = httpx.Client(base_url="http://127.0.0.1:8000")

print("=" * 60)
print("Testing Employee CRUD Endpoints")
print("=" * 60 + "\n")

# Test 1: List employees (should be empty initially)
resp = client.get("/employees/")
print(f"[1] GET /employees/: {resp.status_code}")
print(f"    Data: {resp.json()}\n")

# Test 2: Create an employee
employee_data = {
    "emp_id": "E001",
    "full_name": "Alice Johnson",
    "email": "alice@acme.com",
    "department": "Engineering",
    "country": "US",
    "job_title": "Senior Engineer",
    "band": "L4",
    "employment_type": "full-time",
    "status": "active",
    "base_salary": 150000.0,
    "currency": "USD",
}
resp = client.post("/employees/", json=employee_data)
print(f"[2] POST /employees/: {resp.status_code}")
employee = resp.json()
print(f"    Created employee: ID={employee['id']}, name={employee['full_name']}\n")
emp_id = employee["id"]

# Test 3: Get single employee
resp = client.get(f"/employees/{emp_id}")
print(f"[3] GET /employees/{emp_id}: {resp.status_code}")
print(f"    Name: {resp.json()['full_name']}, Status: {resp.json()['status']}\n")

# Test 4: Update employee with salary change
update_data = {"base_salary": 160000.0, "changed_by": "HR Manager"}
resp = client.put(f"/employees/{emp_id}", json=update_data)
print(f"[4] PUT /employees/{emp_id}: {resp.status_code}")
updated = resp.json()
print(f"    Updated salary to: {updated['base_salary']}\n")

# Test 5: Get salary history
resp = client.get(f"/employees/{emp_id}/salary-history")
print(f"[5] GET /employees/{emp_id}/salary-history: {resp.status_code}")
history = resp.json()
print(f"    History records: {len(history)}")
if history:
    record = history[0]
    print(f"    Latest: {record['previous_salary']} → {record['new_salary']} (by {record['changed_by']})\n")

# Test 6: Deactivate employee
resp = client.delete(f"/employees/{emp_id}")
print(f"[6] DELETE /employees/{emp_id}: {resp.status_code}")
print(f"    Status after deactivation: {resp.json()['status']}\n")

# Test 7: Test duplicate emp_id error
print(f"[7] Testing duplicate emp_id...")
resp = client.post("/employees/", json=employee_data)
print(f"    POST /employees/ (duplicate): {resp.status_code}")
if resp.status_code == 400:
    print(f"    Error: {resp.json()['detail']}\n")

# Test 8: Test 404 on non-existent employee
print(f"[8] Testing 404 on non-existent employee...")
resp = client.get("/employees/99999")
print(f"    GET /employees/99999: {resp.status_code}")
if resp.status_code == 404:
    print(f"    Error: {resp.json()['detail']}\n")

print("=" * 60)
print("All tests completed!")
print("=" * 60)
