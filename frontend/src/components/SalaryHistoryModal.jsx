import { useQuery } from '@tanstack/react-query'
import { LoaderCircle, X } from 'lucide-react'
import { getSalaryHistory } from '../api/employees.js'

function Spinner() {
  return (
    <div className="spinner-wrap" role="status" aria-live="polite">
      <LoaderCircle className="spinner" size={20} />
      <span>Loading salary history...</span>
    </div>
  )
}

function formatDate(value) {
  return new Date(value).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
}

function formatSalary(value) {
  return Number(value).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}

function formatChange(previousSalary, newSalary) {
  const difference = Number(newSalary) - Number(previousSalary)
  const absoluteValue = Math.abs(difference).toLocaleString('en-US', {
    maximumFractionDigits: 0,
  })

  if (difference > 0) {
    return { text: `+${absoluteValue}`, className: 'change-positive' }
  }

  if (difference < 0) {
    return { text: `-${absoluteValue}`, className: 'change-negative' }
  }

  return { text: '0', className: 'change-neutral' }
}

export default function SalaryHistoryModal({ isOpen, onClose, employee }) {
  const salaryHistoryQuery = useQuery({
    queryKey: ['salary-history', employee?.id],
    queryFn: () => getSalaryHistory(employee.id),
    enabled: isOpen && !!employee,
  })

  if (!isOpen || !employee) {
    return null
  }

  return (
    <div className="modal-backdrop" onClick={onClose} role="presentation">
      <div className="modal-card salary-history-modal" onClick={(event) => event.stopPropagation()}>
        <div className="modal-header">
          <div>
            <p className="modal-kicker">Employee salary log</p>
            <h2>Salary History — {employee.full_name}</h2>
          </div>
          <button type="button" className="modal-close" onClick={onClose} aria-label="Close modal">
            <X size={18} />
          </button>
        </div>

        <div className="salary-history-content">
          {salaryHistoryQuery.isLoading ? (
            <Spinner />
          ) : salaryHistoryQuery.isError ? (
            <div className="error-box">Unable to load salary history. Please try again.</div>
          ) : salaryHistoryQuery.data.length === 0 ? (
            <div className="empty-history-state">No salary history found.</div>
          ) : (
            <div className="table-wrap salary-history-table-wrap">
              <table className="salary-history-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Changed By</th>
                    <th>Previous Salary</th>
                    <th>New Salary</th>
                    <th>Change</th>
                    <th>Reason</th>
                  </tr>
                </thead>
                <tbody>
                  {salaryHistoryQuery.data.map((entry) => {
                    const change = formatChange(entry.previous_salary, entry.new_salary)

                    return (
                      <tr key={entry.id}>
                        <td>{formatDate(entry.changed_at)}</td>
                        <td>{entry.changed_by}</td>
                        <td>{formatSalary(entry.previous_salary)}</td>
                        <td>{formatSalary(entry.new_salary)}</td>
                        <td className={change.className}>{change.text}</td>
                        <td>{entry.reason}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}