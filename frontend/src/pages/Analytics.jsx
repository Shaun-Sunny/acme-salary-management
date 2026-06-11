import { useQuery } from '@tanstack/react-query'
import { LoaderCircle } from 'lucide-react'
import {
  Bar,
  BarChart,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import {
  getBandDistribution,
  getHeadcount,
  getSalaryStats,
  getTopEarners,
} from '../api/analytics.js'

const PIE_COLORS = ['#4f46e5', '#7c3aed', '#a855f7', '#c084fc', '#e879f9']

function Spinner() {
  return (
    <div className="spinner-wrap" role="status" aria-live="polite">
      <LoaderCircle className="spinner" size={20} />
      <span>Loading analytics...</span>
    </div>
  )
}

function formatNumber(value) {
  return Number(value).toLocaleString(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })
}

function formatCurrency(value) {
  return `$${formatNumber(value)}`
}

function formatSalary(value, currency) {
  return `${Number(value).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })} ${currency}`
}

function StatCard({ label, value }) {
  return (
    <article className="analytics-stat-card">
      <p>{label}</p>
      <strong>{value}</strong>
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

  const bandDistributionQuery = useQuery({
    queryKey: ['analytics', 'band-distribution'],
    queryFn: getBandDistribution,
  })

  const topEarnersQuery = useQuery({
    queryKey: ['analytics', 'top-earners', 10],
    queryFn: () => getTopEarners(10),
  })

  const isLoading =
    salaryStatsQuery.isLoading ||
    headcountQuery.isLoading ||
    bandDistributionQuery.isLoading ||
    topEarnersQuery.isLoading

  const isError =
    salaryStatsQuery.isError ||
    headcountQuery.isError ||
    bandDistributionQuery.isError ||
    topEarnersQuery.isError

  const overall = salaryStatsQuery.data?.overall ?? {}
  const salaryByDepartment = salaryStatsQuery.data?.by_department ?? []
  const headcountByCountry = headcountQuery.data?.by_country ?? []
  const bandDistribution = bandDistributionQuery.data ?? []
  const topEarners = topEarnersQuery.data ?? []

  return (
    <section className="page-shell analytics-page">
      <div className="page-header analytics-header">
        <div>
          <p className="eyebrow">Analytics dashboard</p>
          <h1>Salary and headcount insights</h1>
          <p className="page-subtitle">
            Track compensation trends, workforce distribution, and top earners across ACME.
          </p>
        </div>
      </div>

      {isLoading ? (
        <div className="panel analytics-panel">
          <Spinner />
        </div>
      ) : isError ? (
        <div className="error-box">Unable to load analytics. Please try again.</div>
      ) : (
        <div className="analytics-dashboard">
          <section className="panel analytics-section">
            <div className="analytics-stats-row">
              <StatCard label="Total Active Employees" value={headcountQuery.data?.total ?? 0} />
              <StatCard label="Average Salary" value={formatCurrency(overall.avg ?? 0)} />
              <StatCard label="Median Salary" value={formatCurrency(overall.median ?? 0)} />
              <StatCard
                label="Salary Range"
                value={`${formatCurrency(overall.min ?? 0)} – ${formatCurrency(overall.max ?? 0)}`}
              />
            </div>
          </section>

          <section className="charts-row">
            <article className="panel analytics-section chart-card">
              <div className="section-title-block">
                <h2>Average Salary by Department</h2>
              </div>
              <div className="chart-area">
                <ResponsiveContainer width="100%" height={320}>
                  <BarChart data={salaryByDepartment}>
                    <XAxis dataKey="department" tickLine={false} axisLine={false} />
                    <YAxis tickLine={false} axisLine={false} tickFormatter={formatCurrency} />
                    <Tooltip formatter={(value) => [formatCurrency(value), 'Average Salary']} />
                    <Bar dataKey="avg" fill="#4f46e5" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </article>

            <article className="panel analytics-section chart-card">
              <div className="section-title-block">
                <h2>Headcount by Country</h2>
              </div>
              <div className="chart-area">
                <ResponsiveContainer width="100%" height={320}>
                  <PieChart>
                    <Pie
                      data={headcountByCountry}
                      dataKey="count"
                      nameKey="country"
                      innerRadius={72}
                      outerRadius={118}
                      paddingAngle={2}
                    >
                      {headcountByCountry.map((entry, index) => (
                        <Cell key={entry.country} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </article>
          </section>

          <section className="panel analytics-section">
            <div className="section-title-block">
              <h2>Band Distribution</h2>
            </div>
            <div className="table-wrap analytics-table-wrap">
              <table className="analytics-table">
                <thead>
                  <tr>
                    <th>Band</th>
                    <th>Employee Count</th>
                    <th>Avg Salary</th>
                    <th>Min Salary</th>
                    <th>Max Salary</th>
                  </tr>
                </thead>
                <tbody>
                  {bandDistribution.map((item) => (
                    <tr key={item.band}>
                      <td>{item.band}</td>
                      <td>{item.count}</td>
                      <td>{Number(item.avg_salary).toLocaleString()}</td>
                      <td>{Number(item.min_salary).toLocaleString()}</td>
                      <td>{Number(item.max_salary).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="panel analytics-section">
            <div className="section-title-block">
              <h2>Top 10 Earners</h2>
            </div>
            <div className="table-wrap analytics-table-wrap">
              <table className="analytics-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Emp ID</th>
                    <th>Full Name</th>
                    <th>Department</th>
                    <th>Band</th>
                    <th>Salary</th>
                    <th>Currency</th>
                  </tr>
                </thead>
                <tbody>
                  {topEarners.map((employee, index) => (
                    <tr key={employee.id}>
                      <td>{index + 1}</td>
                      <td>{employee.emp_id}</td>
                      <td>{employee.full_name}</td>
                      <td>{employee.department}</td>
                      <td>{employee.band}</td>
                      <td>{formatSalary(employee.base_salary, employee.currency)}</td>
                      <td>{employee.currency}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      )}
    </section>
  )
}