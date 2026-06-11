import { useQuery } from '@tanstack/react-query'
import { BarChart3, LoaderCircle, TrendingUp, Trophy, Users } from 'lucide-react'
import {
  getBandDistribution,
  getHeadcount,
  getSalaryStats,
  getTopEarners,
} from '../api/analytics.js'

function Spinner() {
  return (
    <div className="spinner-wrap" role="status" aria-live="polite">
      <LoaderCircle className="spinner" size={20} />
      <span>Loading analytics...</span>
    </div>
  )
}

function formatMoney(value) {
  return Number(value).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}

function MetricCard({ icon: Icon, label, value, accent }) {
  return (
    <article className={`metric-card ${accent}`}>
      <div className="metric-icon">
        <Icon size={18} />
      </div>
      <div>
        <p className="metric-label">{label}</p>
        <h2 className="metric-value">{value}</h2>
      </div>
    </article>
  )
}

export default function Analytics() {
  const salaryStatsQuery = useQuery({
    queryKey: ['analytics', 'salary-stats'],
    queryFn: getSalaryStats,
  })

  const headcountQuery = useQuery({
    queryKey: ['analytics', 'headcount'],
    queryFn: getHeadcount,
  })

  const bandQuery = useQuery({
    queryKey: ['analytics', 'band-distribution'],
    queryFn: getBandDistribution,
  })

  const topEarnersQuery = useQuery({
    queryKey: ['analytics', 'top-earners', 10],
    queryFn: () => getTopEarners(10),
  })

  const isPending =
    salaryStatsQuery.isPending ||
    headcountQuery.isPending ||
    bandQuery.isPending ||
    topEarnersQuery.isPending

  const isError =
    salaryStatsQuery.isError ||
    headcountQuery.isError ||
    bandQuery.isError ||
    topEarnersQuery.isError

  return (
    <section className="page-shell">
      <div className="page-header analytics-header">
        <div>
          <p className="eyebrow">Analytics dashboard</p>
          <h1>Salary and headcount insights</h1>
          <p className="page-subtitle">
            Quick answers for compensation, workforce distribution, and top earners.
          </p>
        </div>
      </div>

      {isPending ? (
        <div className="panel analytics-panel">
          <Spinner />
        </div>
      ) : isError ? (
        <div className="error-box">Unable to load analytics right now.</div>
      ) : (
        <div className="analytics-grid">
          <section className="analytics-stack">
            <div className="metric-grid">
              <MetricCard icon={Users} label="Active headcount" value={headcountQuery.data.total} accent="teal" />
              <MetricCard
                icon={TrendingUp}
                label="Average salary"
                value={formatMoney(salaryStatsQuery.data.overall.avg)}
                accent="amber"
              />
              <MetricCard
                icon={BarChart3}
                label="Median salary"
                value={formatMoney(salaryStatsQuery.data.overall.median)}
                accent="slate"
              />
              <MetricCard
                icon={Trophy}
                label="Highest salary"
                value={formatMoney(salaryStatsQuery.data.overall.max)}
                accent="rose"
              />
            </div>

            <section className="panel analytics-panel">
              <h2>Headcount by department</h2>
              <div className="stack-list">
                {headcountQuery.data.by_department.map((item) => (
                  <div key={item.department} className="stack-row">
                    <span>{item.department}</span>
                    <strong>{item.count}</strong>
                  </div>
                ))}
              </div>
            </section>

            <section className="panel analytics-panel">
              <h2>Band distribution</h2>
              <div className="stack-list">
                {bandQuery.data.map((item) => (
                  <div key={item.band} className="stack-row">
                    <span>
                      {item.band} · {item.count} employees
                    </span>
                    <strong>{formatMoney(item.avg_salary)}</strong>
                  </div>
                ))}
              </div>
            </section>
          </section>

          <section className="analytics-stack">
            <section className="panel analytics-panel">
              <h2>Salary breakdown</h2>
              <div className="stack-list">
                <div className="stack-row">
                  <span>Average</span>
                  <strong>{formatMoney(salaryStatsQuery.data.overall.avg)}</strong>
                </div>
                <div className="stack-row">
                  <span>Median</span>
                  <strong>{formatMoney(salaryStatsQuery.data.overall.median)}</strong>
                </div>
                <div className="stack-row">
                  <span>Minimum</span>
                  <strong>{formatMoney(salaryStatsQuery.data.overall.min)}</strong>
                </div>
                <div className="stack-row">
                  <span>Maximum</span>
                  <strong>{formatMoney(salaryStatsQuery.data.overall.max)}</strong>
                </div>
              </div>
            </section>

            <section className="panel analytics-panel">
              <h2>Top earners</h2>
              <div className="top-earners-list">
                {topEarnersQuery.data.map((employee, index) => (
                  <div key={employee.id} className="top-earner-row">
                    <span className="rank-pill">{index + 1}</span>
                    <div>
                      <strong>{employee.full_name}</strong>
                      <p>
                        {employee.department} · {employee.band}
                      </p>
                    </div>
                    <span className="earnings">
                      {formatMoney(employee.base_salary)} {employee.currency}
                    </span>
                  </div>
                ))}
              </div>
            </section>
          </section>
        </div>
      )}
    </section>
  )
}
