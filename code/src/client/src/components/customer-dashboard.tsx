"use client"

import { useState, useEffect } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import CustomerPurchaseHistory from "@/components/customer-purchase-history"
import CustomerSupportHistory from "@/components/customer-support-history"
import CustomerSocialMedia from "@/components/customer-social-media"
import CustomerInformation from "@/components/customer-information"
import { RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { CustomerInfo, useCustomerIds, useCustomerInfo } from "@/lib/api"

// Updated mock customer data with new fields
const CUSTOMERS = [
    {
        customer_id: "CUST_1",
        age: 24,
        gender: "Female",
        education: "Graduate",
        is_married: false,
        num_of_children: 0,
        location: "California",
        income: 65000,
        job: "Software Engineer",
        goals: ["stability", "save for down payment on house"],
        credit_score: 720,
        preferred_payment_method: "Credit Card",
        balance: [5200.5, 5500.75, 5850.2, 6200.9, 6500.1, 7000.5, 7800.0, 8500.3, 9200.8, 10000.0, 11000.5, 3000.0],
        loan_amts: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        monthly_spending: [1500, 1600, 1550, 1700, 1650, 1750, 1800, 1850, 1900, 1950, 2000, 2100],
        main_purchase_cat: ["Rent", "Groceries", "Restaurants", "Travel", "Utilities"],
        support_interaction_count: 2,
        satisfaction: 8,
    },
    {
        customer_id: "CUST_2",
        age: 35,
        gender: "Male",
        education: "Graduate",
        is_married: true,
        num_of_children: 2,
        location: "Texas",
        income: 120000,
        job: "Project Manager",
        goals: ["stability", "children's education", "retirement"],
        credit_score: 780,
        preferred_payment_method: "Debit Card",
        balance: [
            20000.0, 21000.5, 22500.25, 23000.75, 22000.0, 23500.5, 24000.0, 25000.75, 26000.25, 27000.0, 28000.5, 29000.0,
        ],
        loan_amts: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15000],
        monthly_spending: [3500, 3600, 3700, 3800, 3500, 3700, 3800, 3900, 4000, 4100, 4200, 4300],
        main_purchase_cat: ["Mortgage", "Groceries", "Childcare", "Utilities", "Entertainment"],
        support_interaction_count: 5,
        satisfaction: 7.2,
    },
]

export default function CustomerDashboard() {
    const { data: customerIds, isLoading: isCustomerIdsLoading } = useCustomerIds();
    const [selectedCustomerId, setSelectedCustomerId] = useState<string | undefined>()
    const { data: customerInfo, isLoading: isCustomerLoading } = useCustomerInfo(selectedCustomerId || "");

    return (
        <div className="container mx-auto py-6">
            <h1 className="text-3xl font-bold mb-6">Customer Dashboard</h1>

            <Card className="mb-6">
                <CardHeader>
                    <CardTitle>Select Customer</CardTitle>
                    <CardDescription>Choose a customer to view their information</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex items-end gap-2">
                        <div className="grid w-full max-w-sm items-center gap-1.5">
                            <Label htmlFor="customer">Customer</Label>
                            <Select value={selectedCustomerId} onValueChange={setSelectedCustomerId} disabled={isCustomerIdsLoading}>
                                <SelectTrigger id="customer">
                                    <SelectValue placeholder="Select a customer" />
                                </SelectTrigger>
                                <SelectContent>
                                    {customerIds?.map((id) => (
                                        <SelectItem key={id} value={id}>
                                            {id}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                        {customerInfo && <Button
                            variant="outline"
                            size="icon"
                            onClick={() => {
                                // TODO: refresh customer data
                            }}
                            disabled={isCustomerLoading}
                        >
                            <RefreshCw className={`h-4 w-4 ${isCustomerLoading ? "animate-spin" : ""}`} />
                            <span className="sr-only">Refresh customer data</span>
                        </Button>}
                    </div>
                </CardContent>
            </Card>

            {selectedCustomerId && customerInfo ? (
                <>
                    <div className="mb-6">
                        <CustomerInformation customer={customerInfo} />
                    </div>
                    <Tabs defaultValue="purchases" className="w-full">
                        <TabsList className="grid w-full grid-cols-3">
                            <TabsTrigger value="purchases">Purchase History</TabsTrigger>
                            <TabsTrigger value="support">Support History</TabsTrigger>
                            <TabsTrigger value="social">Social Media</TabsTrigger>
                        </TabsList>
                        <TabsContent value="purchases">
                            <CustomerPurchaseHistory customerId={selectedCustomerId} />
                        </TabsContent>
                        <TabsContent value="support">
                            <CustomerSupportHistory customerId={selectedCustomerId} />
                        </TabsContent>
                        <TabsContent value="social">
                            <CustomerSocialMedia customerId={selectedCustomerId} />
                        </TabsContent>
                    </Tabs>
                </>
            ) : (
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-center text-muted-foreground">Please select a customer to view their information</p>
                    </CardContent>
                </Card>
            )}
        </div>
    )
}

