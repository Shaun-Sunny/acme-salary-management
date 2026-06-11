import { useEffect, useState } from 'react'
import { X } from 'lucide-react'
import { createEmployee, updateEmployee } from '../api/employees.js'

const DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'Finance', 'HR', 'Operations', 'Legal']
const COUNTRIES = ['United States', 'United Kingdom', 'India', 'Germany', 'United Arab Emirates']
const BANDS = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6']
const EMPLOYMENT_TYPES = ['full-time', 'contractor']
const STATUSES = ['active', 'inactive']
const CURRENCIES = ['USD', 'GBP', 'INR', 'EUR', 'AED']

const baseFormState = {
  emp_id: '',
  full_name: '',
  email: '',
  department: 'Engineering',
  country: 'United States',
  job_title: '',
  band: 'L1',
  employment_type: 'full-time',
  status: 'active',
  base_salary: '',
  currency: 'USD',
  changed_by: 'HR Manager',
  reason_for_change: '',
}

function buildInitialState(employee) {
  if (!employee) {
    return baseFormState
  }

  return {
    emp_id: employee.emp_id ?? '',
    full_name: employee.full_name ?? '',
    email: employee.email ?? '',
    department: employee.department ?? 'Engineering',
    country: employee.country ?? 'United States',
    job_title: employee.job_title ?? '',
    band: employee.band ?? 'L1',
    employment_type: employee.employment_type ?? 'full-time',
    status: employee.status ?? 'active',
    base_salary: employee.base_salary ?? '',
    currency: employee.currency ?? 'USD',
    changed_by: 'HR Manager',
    reason_for_change: '',
  }
}

function buildPayload(formData, employee) {
  const payload = {
    emp_id: formData.emp_id.trim(),
    full_name: formData.full_name.trim(),
    email: formData.email.trim(),
    department: formData.department,
    country: formData.country,
    job_title: formData.job_title.trim(),
    band: formData.band,
    employment_type: formData.employment_type,
    status: formData.status,
    base_salary: Number(formData.base_salary),
    currency: formData.currency,
  }

  if (employee) {
    payload.changed_by = formData.changed_by.trim() || 'HR Manager'
    payload.reason_for_change = formData.reason_for_change.trim()
  }

  return payload
}

export default function EmployeeForm({ isOpen, onClose, onSuccess, employee }) {
  const [formData, setFormData] = useState(() => buildInitialState(employee))
  const [errors, setErrors] = useState({})
  const [apiError, setApiError] = useState('')
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    if (isOpen) {
      setFormData(buildInitialState(employee))
      setErrors({})
      setApiError('')
      setIsSaving(false)
    }
  }, [employee, isOpen])

  if (!isOpen) {
    return null
  }

  const isEditMode = Boolean(employee)

  function updateField(name, value) {
    setFormData((current) => ({ ...current, [name]: value }))
    setErrors((current) => ({ ...current, [name]: '' }))
    setApiError('')
  }

  function validate() {
    const nextErrors = {}

    if (!formData.emp_id.trim()) nextErrors.emp_id = 'Emp ID is required.'
    if (!formData.full_name.trim()) nextErrors.full_name = 'Full Name is required.'
    if (!formData.email.trim()) nextErrors.email = 'Email is required.'
    if (!formData.job_title.trim()) nextErrors.job_title = 'Job Title is required.'
    if (formData.base_salary === '' || Number.isNaN(Number(formData.base_salary))) {
      nextErrors.base_salary = 'Base Salary is required.'
    } else if (Number(formData.base_salary) < 0) {
      nextErrors.base_salary = 'Base Salary must be 0 or greater.'
    }

    if (isEditMode && !formData.changed_by.trim()) {
      nextErrors.changed_by = 'Changed By is required.'
    }

    if (isEditMode && !formData.reason_for_change.trim()) {
      nextErrors.reason_for_change = 'Reason for Change is required.'
    }

    setErrors(nextErrors)
    return Object.keys(nextErrors).length === 0
  }

  async function handleSubmit(event) {
    event.preventDefault()

    if (!validate()) {
      return
    }

    const payload = buildPayload(formData, employee)

    setIsSaving(true)
    setApiError('')

    try {
      if (employee) {
        await updateEmployee(employee.id, payload)
      } else {
        await createEmployee(payload)
      }

      onSuccess()
      onClose()
    } catch (error) {
      const message = error?.response?.data?.detail || error?.message || 'Unable to save employee.'
      setApiError(message)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose} role="presentation">
      <div className="modal-card" onClick={(event) => event.stopPropagation()}>
        <div className="modal-header">
          <h2>{isEditMode ? 'Edit Employee' : 'Add Employee'}</h2>
          <button type="button" className="modal-close" onClick={onClose} aria-label="Close modal">
            <X size={18} />
          </button>
        </div>

        <form className="employee-form" onSubmit={handleSubmit}>
          <div className="form-grid">
            <label className="field">
              <span>Emp ID</span>
              <input
                type="text"
                value={formData.emp_id}
                onChange={(event) => updateField('emp_id', event.target.value)}
                disabled={isEditMode}
                required
              />
              {errors.emp_id ? <small className="field-error">{errors.emp_id}</small> : null}
            </label>

            <label className="field">
              <span>Full Name</span>
              <input
                type="text"
                value={formData.full_name}
                onChange={(event) => updateField('full_name', event.target.value)}
                required
              />
              {errors.full_name ? <small className="field-error">{errors.full_name}</small> : null}
            </label>

            <label className="field">
              <span>Email</span>
              <input
                type="email"
                value={formData.email}
                onChange={(event) => updateField('email', event.target.value)}
                required
              />
              {errors.email ? <small className="field-error">{errors.email}</small> : null}
            </label>

            <label className="field">
              <span>Department</span>
              <select value={formData.department} onChange={(event) => updateField('department', event.target.value)}>
                {DEPARTMENTS.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>

            <label className="field">
              <span>Country</span>
              <select value={formData.country} onChange={(event) => updateField('country', event.target.value)}>
                {COUNTRIES.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>

            <label className="field">
              <span>Job Title</span>
              <input
                type="text"
                value={formData.job_title}
                onChange={(event) => updateField('job_title', event.target.value)}
                required
              />
              {errors.job_title ? <small className="field-error">{errors.job_title}</small> : null}
            </label>

            <label className="field">
              <span>Band</span>
              <select value={formData.band} onChange={(event) => updateField('band', event.target.value)}>
                {BANDS.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>

            <label className="field">
              <span>Employment Type</span>
              <select
                value={formData.employment_type}
                onChange={(event) => updateField('employment_type', event.target.value)}
              >
                {EMPLOYMENT_TYPES.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>

            <label className="field">
              <span>Status</span>
              <select value={formData.status} onChange={(event) => updateField('status', event.target.value)}>
                {STATUSES.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>

            <label className="field">
              <span>Base Salary</span>
              <input
                type="number"
                min="0"
                step="0.01"
                value={formData.base_salary}
                onChange={(event) => updateField('base_salary', event.target.value)}
                required
              />
              {errors.base_salary ? <small className="field-error">{errors.base_salary}</small> : null}
            </label>

            <label className="field">
              <span>Currency</span>
              <select value={formData.currency} onChange={(event) => updateField('currency', event.target.value)}>
                {CURRENCIES.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>

            {isEditMode ? (
              <label className="field">
                <span>Changed By</span>
                <input
                  type="text"
                  placeholder="HR Manager"
                  value={formData.changed_by}
                  onChange={(event) => updateField('changed_by', event.target.value)}
                />
                {errors.changed_by ? <small className="field-error">{errors.changed_by}</small> : null}
              </label>
            ) : null}

            {isEditMode ? (
              <label className="field">
                <span>Reason for Change</span>
                <input
                  type="text"
                  placeholder="e.g. Annual review"
                  value={formData.reason_for_change}
                  onChange={(event) => updateField('reason_for_change', event.target.value)}
                />
                {errors.reason_for_change ? <small className="field-error">{errors.reason_for_change}</small> : null}
              </label>
            ) : null}
          </div>

          {apiError ? <div className="form-error-banner">{apiError}</div> : null}

          <div className="modal-actions">
            <button type="button" className="secondary-button" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="primary-button" disabled={isSaving}>
              {isSaving ? 'Saving...' : 'Save Employee'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}