import { useMemo, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { LoaderCircle, Pencil, Search, X } from 'lucide-react'
import { deactivateEmployee, getEmployees } from '../api/employees.js'

const PAGE_SIZE = 50

const FILTER_OPTIONS = {
  department: ['Engineering', 'Product', 'Sales', 'Marketing', 'Finance', 'HR', 'Operations', 'Legal'],
  country: ['United States', 'United Kingdom', 'India', 'Germany', 'United Arab Emirates'],
  band: ['L1', 'L2', 'L3', 'L4', 'L5', 'L6'],
  status: ['active', 'inactive'],
}

const defaultFilters = {
  search: '',
  department: '',
  country: '',
  band: '',
  status: '',
}

function formatSalary(value, currency) {
  return `${Number(value).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })} ${currency}`
}

function buildParams(filters, page) {
  return {
    skip: (page - 1) * PAGE_SIZE,
    limit: PAGE_SIZE,
    search: filters.search.trim() || undefined,
    department: filters.department || undefined,
    country: filters.country || undefined,
    band: filters.band || undefined,
    status: filters.status || undefined,
  }
}

async function fetchEmployeeCount(filters) {
  let total = 0
  let skip = 0

  while (true) {
    const batch = await getEmployees({
      ...buildParams(filters, 1),
      skip,
      limit: 1000,
    })

    total += batch.length

    if (batch.length < 1000) {
      break
    }

    skip += 1000
  }

  return total
}

function Spinner() {
  return (
    <div className="spinner-wrap" role="status" aria-live="polite">
      <LoaderCircle className="spinner" size={20} />
      <span>Loading employees...</span>
    </div>
  )
}

export default function Employees() {
  const [page, setPage] = useState(1)
  const [filters, setFilters] = useState(defaultFilters)
  const queryClient = useQueryClient()

  const normalizedFilters = useMemo(
    () => ({
      search: filters.search,
      department: filters.department,
      country: filters.country,
      band: filters.band,
      status: filters.status,
    }),
    [filters],
  )

  const employeesQuery = useQuery({
    queryKey: ['employees', 'page', normalizedFilters, page],
    queryFn: () => getEmployees(buildParams(normalizedFilters, page)),
    keepPreviousData: true,
  })

  const countQuery = useQuery({
    queryKey: ['employees', 'count', normalizedFilters],
    queryFn: () => fetchEmployeeCount(normalizedFilters),
  })

  const deactivateMutation = useMutation({
    mutationFn: deactivateEmployee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] })
    },
  })

  const employees = employeesQuery.data ?? []
  const total = countQuery.data ?? 0
  const start = total === 0 ? 0 : (page - 1) * PAGE_SIZE + 1
  const end = Math.min(page * PAGE_SIZE, total)
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE))

  function updateFilter(name, value) {
    setPage(1)
    setFilters((current) => ({ ...current, [name]: value }))
  }

  function clearFilters() {
    setPage(1)
    setFilters(defaultFilters)
  }

  async function handleDeactivate(id) {
    await deactivateMutation.mutateAsync(id)
  }

  return (
    <section className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Employee directory</p>
          <h1>Manage salary records at ACME</h1>
          <p className="page-subtitle">
            Search, filter, update, and deactivate employee records from one place.
          </p>
        </div>

        <button type="button" className="primary-button" onClick={() => console.log('Add Employee clicked')}>
          Add Employee
        </button>
      </div>

      <div className="panel filter-panel">
        <div className="filter-search">
          <Search size={18} />
          <input
            type="search"
            placeholder="Search by name or email"
            value={filters.search}
            onChange={(event) => updateFilter('search', event.target.value)}
          />
        </div>

        <div className="filter-grid">
          <select value={filters.department} onChange={(event) => updateFilter('department', event.target.value)}>
            <option value="">Department</option>
            {FILTER_OPTIONS.department.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          <select value={filters.country} onChange={(event) => updateFilter('country', event.target.value)}>
            <option value="">Country</option>
            {FILTER_OPTIONS.country.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          <select value={filters.band} onChange={(event) => updateFilter('band', event.target.value)}>
            <option value="">Band</option>
            {FILTER_OPTIONS.band.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          <select value={filters.status} onChange={(event) => updateFilter('status', event.target.value)}>
            <option value="">Status</option>
            {FILTER_OPTIONS.status.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-actions">
          <button type="button" className="secondary-button" onClick={clearFilters}>
            Clear filters
          </button>
        </div>
      </div>

      <div className="panel table-panel">
        {employeesQuery.isPending || countQuery.isPending ? (
          <Spinner />
        ) : employeesQuery.isError || countQuery.isError ? (
          <div className="error-box">Unable to load employees. Please try again.</div>
        ) : (
          <>
            <div className="table-meta">
              <span>
                Showing {start}–{end} of {total} employees
              </span>
              {deactivateMutation.isPending ? <span className="muted">Updating employee status...</span> : null}
            </div>

            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Emp ID</th>
                    <th>Full Name</th>
                    <th>Department</th>
                    <th>Country</th>
                    <th>Band</th>
                    <th>Job Title</th>
                    <th>Status</th>
                    <th>Salary</th>
                    <th>Currency</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {employees.length === 0 ? (
                    <tr>
                      <td colSpan="10" className="empty-state">
                        No employees match the current filters.
                      </td>
                    </tr>
                  ) : (
                    employees.map((employee) => (
                      <tr key={employee.id}>
                        <td>{employee.emp_id}</td>
                        <td>
                          <div className="employee-name">{employee.full_name}</div>
                          <div className="employee-email">{employee.email}</div>
                        </td>
                        <td>{employee.department}</td>
                        <td>{employee.country}</td>
                        <td>{employee.band}</td>
                        <td>{employee.job_title}</td>
                        <td>
                          <span className={`status-pill ${employee.status}`}>{employee.status}</span>
                        </td>
                        <td>{formatSalary(employee.base_salary, employee.currency)}</td>
                        <td>{employee.currency}</td>
                        <td>
                          <div className="action-group">
                            <button
                              type="button"
                              className="icon-button"
                              onClick={() => console.log('Edit employee', employee.id)}
                              aria-label={`Edit ${employee.full_name}`}
                            >
                              <Pencil size={16} />
                            </button>
                            {employee.status === 'active' ? (
                              <button
                                type="button"
                                className="icon-button danger"
                                onClick={() => handleDeactivate(employee.id)}
                                aria-label={`Deactivate ${employee.full_name}`}
                                disabled={deactivateMutation.isPending}
                              >
                                <X size={16} />
                              </button>
                            ) : null}
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            <div className="pagination-row">
              <button
                type="button"
                className="secondary-button"
                disabled={page <= 1}
                onClick={() => setPage((current) => Math.max(1, current - 1))}
              >
                Previous
              </button>

              <span>
                Page {page} of {totalPages}
              </span>

              <button
                type="button"
                className="secondary-button"
                disabled={page >= totalPages}
                onClick={() => setPage((current) => current + 1)}
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </section>
  )
}
