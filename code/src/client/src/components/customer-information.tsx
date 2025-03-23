import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { User, Briefcase, MapPin, GraduationCap, DollarSign, CreditCard, Heart, Target } from "lucide-react"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"

interface CustomerInformationProps {
  customer: {
    customer_id: string
    age: number
    gender: string
    education: string
    is_married: boolean
    num_of_children: number
    location: string
    income: number
    job: string
    goals: string[]
    credit_score: number
    preferred_payment_method: string
    balance: number[]
    loan_amts: number[]
    monthly_spending: number[]
    main_purchase_cat: string[]
    support_interaction_count: number
    satisfaction: number
  }
}

export default function CustomerInformation({ customer }: CustomerInformationProps) {
  const [activeTab, setActiveTab] = useState("overview")

  // Format income with commas
  const formattedIncome = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(customer.income)

  // Format current balance (last item in the array)
  const currentBalance = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  }).format(customer.balance[customer.balance.length - 1])

  // Format current loan amount (last item in the array)
  const currentLoan = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  }).format(customer.loan_amts[customer.loan_amts.length - 1])

  // Format current monthly spending (last item in the array)
  const currentMonthlySpending = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 0,
  }).format(customer.monthly_spending[customer.monthly_spending.length - 1])

  // Calculate credit score color and percentage
  const getCreditScoreColor = (score: number) => {
    if (score >= 750) return "bg-green-500"
    if (score >= 700) return "bg-green-400"
    if (score >= 650) return "bg-yellow-400"
    if (score >= 600) return "bg-orange-400"
    return "bg-red-500"
  }

  const creditScorePercentage = (customer.credit_score / 850) * 100

  // Calculate satisfaction color and percentage
  const getSatisfactionColor = (score: number) => {
    if (score >= 9) return "bg-green-500"
    if (score >= 7) return "bg-green-400"
    if (score >= 5) return "bg-yellow-400"
    if (score >= 3) return "bg-orange-400"
    return "bg-red-500"
  }

  const satisfactionPercentage = (customer.satisfaction / 10) * 100

  return (
    <Card>
      <CardHeader>
        <CardTitle>Customer Profile: {customer.customer_id}</CardTitle>
        <CardDescription>Comprehensive customer information and financial overview</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
          <TabsList className="grid grid-cols-3">
            <TabsTrigger value="overview">Personal Overview</TabsTrigger>
            <TabsTrigger value="financial">Financial Profile</TabsTrigger>
            <TabsTrigger value="insights">Customer Insights</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <User className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium leading-none">Demographics</p>
                    <p className="text-sm text-muted-foreground">
                      {customer.age} years old, {customer.gender}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Heart className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium leading-none">Family Status</p>
                    <p className="text-sm text-muted-foreground">
                      {customer.is_married ? "Married" : "Single"},
                      {customer.num_of_children > 0
                        ? ` ${customer.num_of_children} ${customer.num_of_children === 1 ? "child" : "children"}`
                        : " No children"}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <MapPin className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium leading-none">Location</p>
                    <p className="text-sm text-muted-foreground">{customer.location}</p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <GraduationCap className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium leading-none">Education</p>
                    <p className="text-sm text-muted-foreground">{customer.education}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <Briefcase className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium leading-none">Occupation</p>
                    <p className="text-sm text-muted-foreground">{customer.job}</p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <DollarSign className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium leading-none">Annual Income</p>
                    <p className="text-sm text-muted-foreground">{formattedIncome}</p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Target className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium leading-none">Financial Goals</p>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {customer.goals.map((goal, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {goal}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <CreditCard className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium leading-none">Preferred Payment</p>
                    <p className="text-sm text-muted-foreground">{customer.preferred_payment_method}</p>
                  </div>
                </div>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="financial" className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium mb-1">Current Balance</p>
                  <p className="text-2xl font-bold">{currentBalance}</p>
                  <p className="text-xs text-muted-foreground">
                    {customer.balance[customer.balance.length - 1] > customer.balance[customer.balance.length - 2]
                      ? "↑ Increased from last month"
                      : "↓ Decreased from last month"}
                  </p>
                </div>

                <div>
                  <p className="text-sm font-medium mb-1">Current Loan</p>
                  <p className="text-2xl font-bold">{currentLoan}</p>
                </div>

                <div>
                  <p className="text-sm font-medium mb-1">Monthly Spending</p>
                  <p className="text-2xl font-bold">{currentMonthlySpending}</p>
                  <p className="text-xs text-muted-foreground">
                    {customer.monthly_spending[customer.monthly_spending.length - 1] >
                    customer.monthly_spending[customer.monthly_spending.length - 2]
                      ? "↑ Increased from last month"
                      : "↓ Decreased from last month"}
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-1">
                    <p className="text-sm font-medium">Credit Score</p>
                    <p className="text-sm font-medium">{customer.credit_score}</p>
                  </div>
                  <Progress
                    value={creditScorePercentage}
                    className="h-2"
                    indicatorClassName={getCreditScoreColor(customer.credit_score)}
                  />
                  <p className="text-xs text-muted-foreground mt-1">
                    {customer.credit_score >= 750
                      ? "Excellent"
                      : customer.credit_score >= 700
                        ? "Very Good"
                        : customer.credit_score >= 650
                          ? "Good"
                          : customer.credit_score >= 600
                            ? "Fair"
                            : "Poor"}
                  </p>
                </div>

                <div>
                  <p className="text-sm font-medium mb-1">Main Purchase Categories</p>
                  <div className="flex flex-wrap gap-1">
                    {customer.main_purchase_cat.map((category, index) => (
                      <Badge key={index} className="text-xs">
                        {category}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div>
                  <p className="text-sm font-medium mb-1">Balance Trend (12 months)</p>
                  <div className="h-20 flex items-end gap-1">
                    {customer.balance.map((amount, index) => {
                      const height = (amount / Math.max(...customer.balance)) * 100
                      return (
                        <div
                          key={index}
                          className="bg-primary/80 hover:bg-primary transition-colors rounded-t w-full"
                          style={{ height: `${height}%` }}
                          title={`Month ${index + 1}: ${new Intl.NumberFormat("en-US", {
                            style: "currency",
                            currency: "USD",
                          }).format(amount)}`}
                        />
                      )
                    })}
                  </div>
                </div>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="insights" className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium mb-1">Customer Satisfaction</p>
                  <div className="flex items-center gap-2">
                    <Progress
                      value={satisfactionPercentage}
                      className="h-2"
                      indicatorClassName={getSatisfactionColor(customer.satisfaction)}
                    />
                    <span className="text-sm font-medium">{customer.satisfaction}/10</span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    {customer.satisfaction >= 9
                      ? "Extremely Satisfied"
                      : customer.satisfaction >= 7
                        ? "Very Satisfied"
                        : customer.satisfaction >= 5
                          ? "Satisfied"
                          : customer.satisfaction >= 3
                            ? "Somewhat Dissatisfied"
                            : "Dissatisfied"}
                  </p>
                </div>

                <div>
                  <p className="text-sm font-medium mb-1">Support Interactions</p>
                  <p className="text-2xl font-bold">{customer.support_interaction_count}</p>
                  <p className="text-xs text-muted-foreground">
                    {customer.support_interaction_count > 3
                      ? "Above average number of support requests"
                      : "Below average number of support requests"}
                  </p>
                </div>

                <div>
                  <p className="text-sm font-medium mb-1">Spending vs. Income</p>
                  <p className="text-lg">
                    {(
                      ((customer.monthly_spending[customer.monthly_spending.length - 1] * 12) / customer.income) *
                      100
                    ).toFixed(1)}
                    % of income
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {(customer.monthly_spending[customer.monthly_spending.length - 1] * 12) / customer.income < 0.5
                      ? "Healthy spending ratio"
                      : "High spending relative to income"}
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium mb-1">Monthly Spending Trend</p>
                  <div className="h-20 flex items-end gap-1">
                    {customer.monthly_spending.map((amount, index) => {
                      const height = (amount / Math.max(...customer.monthly_spending)) * 100
                      return (
                        <div
                          key={index}
                          className="bg-blue-500/80 hover:bg-blue-500 transition-colors rounded-t w-full"
                          style={{ height: `${height}%` }}
                          title={`Month ${index + 1}: ${new Intl.NumberFormat("en-US", {
                            style: "currency",
                            currency: "USD",
                          }).format(amount)}`}
                        />
                      )
                    })}
                  </div>
                </div>

                <div>
                  <p className="text-sm font-medium mb-1">Customer Value Assessment</p>
                  <div className="flex items-center gap-2 mt-2">
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                    <p className="text-sm">
                      {customer.balance[customer.balance.length - 1] > 10000 && customer.credit_score > 750
                        ? "High-Value Customer"
                        : customer.balance[customer.balance.length - 1] > 5000 && customer.credit_score > 700
                          ? "Medium-Value Customer"
                          : "Growth Potential Customer"}
                    </p>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1 ml-5">
                    Based on balance, credit score, and spending patterns
                  </p>
                </div>

                <div>
                  <p className="text-sm font-medium mb-1">Recommended Actions</p>
                  <ul className="text-sm list-disc pl-5 space-y-1">
                    {customer.credit_score < 700 && <li>Credit improvement consultation</li>}
                    {customer.goals.includes("save for down payment on house") && (
                      <li>Home savings account offering</li>
                    )}
                    {customer.goals.includes("children's education") && <li>Education savings plan</li>}
                    {customer.goals.includes("retirement") && <li>Retirement planning consultation</li>}
                    {customer.satisfaction < 8 && <li>Customer satisfaction follow-up</li>}
                    {customer.support_interaction_count > 3 && <li>Service quality review</li>}
                    {customer.loan_amts[customer.loan_amts.length - 1] > 0 && <li>Loan refinancing options</li>}
                  </ul>
                </div>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}

