"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import CustomerPurchaseHistory from "@/components/customer-purchase-history"
import CustomerSupportHistory from "@/components/customer-support-history"
import CustomerSocialMedia from "@/components/customer-social-media"
import CustomerInformation from "@/components/customer-information"
import { Button } from "@/components/ui/button"
import { useCustomerIds, useCustomerInfo, useCustomerRunAi } from "@/lib/api"

export default function CustomerDashboard() {
    const { data: customerIds, isLoading: isCustomerIdsLoading } = useCustomerIds();
    const [selectedCustomerId, setSelectedCustomerId] = useState<string | undefined>();
    const { data: customerInfo, isLoading: isCustomerLoading } = useCustomerInfo(selectedCustomerId || "");
    const { mutate: runAi, isPending: isRunningAi } = useCustomerRunAi()

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
                        {
                            customerInfo &&
                            <Button
                                variant="outline"
                                onClick={() => {
                                    runAi({ customerId: selectedCustomerId! })
                                }}
                                disabled={isCustomerLoading || isRunningAi}
                                className="flex items-center gap-2"
                            >
                                <span role="img" aria-label="robot">
                                    🤖
                                </span>
                                <span>Run AI</span>
                                {isCustomerLoading || isRunningAi && <span className="ml-2 animate-spin">⟳</span>}
                            </Button>
                        }
                    </div>
                </CardContent>
            </Card>

            {selectedCustomerId && customerInfo ? (
                <>
                    <div className="mb-6">
                        {"error" in customerInfo ? (
                            <p className="text-center text-muted-foreground">{customerInfo.error}</p>
                        ) : (
                            <CustomerInformation customer={customerInfo} />
                        )}
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

