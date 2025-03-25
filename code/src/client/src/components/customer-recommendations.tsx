"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Loader2, Star, AlertCircle, DollarSign, TrendingUp, ShieldCheck } from "lucide-react"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

// Import product data
import { CustomerInfo } from "@/lib/api"
import { getProduct } from "@/lib/financial_products"

interface CustomerRecommendationsProps {
    customerInfo: CustomerInfo
}

const TOP_PRODUCTS_TO_SHOW = 5;
const TOP_PASSIVE_PRODUCTS_TO_SHOW = 5;

export default function CustomerRecommendations({ customerInfo }: CustomerRecommendationsProps) {
    const topProducts = customerInfo.top_n_products.map(getProduct);
    const topPassiveProducts = customerInfo.top_n_passive_products.map(getProduct);

    const recommendations = [
        {
            name: "Top Products",
            products: topProducts.slice(0, TOP_PRODUCTS_TO_SHOW)
        },
        {
            name: "Top Passive Products",
            products: topPassiveProducts.slice(0, TOP_PASSIVE_PRODUCTS_TO_SHOW)
        }
    ]

    // Get tier color
    const getTierColor = (tier: string) => {
        switch (tier) {
            case "Entry":
                return "bg-blue-100 text-blue-800"
            case "Standard":
                return "bg-green-100 text-green-800"
            case "Premium":
                return "bg-purple-100 text-purple-800"
            case "Elite":
                return "bg-amber-100 text-amber-800"
            default:
                return "bg-gray-100 text-gray-800"
        }
    }

    // Format currency
    const formatCurrency = (amount: number) => {
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
            minimumFractionDigits: 0,
            maximumFractionDigits: 0,
        }).format(amount)
    }

    // Render product details based on category
    const renderProductDetails = (product: any) => {
        switch (product.category) {
            case "Credit Card":
                return (
                    <div className="grid grid-cols-2 gap-2 text-sm mt-2">
                        <div>
                            <p className="text-muted-foreground">Interest Rate</p>
                            <p className="font-medium">{product.details.interest_rate}%</p>
                        </div>
                        <div>
                            <p className="text-muted-foreground">Annual Fee</p>
                            <p className="font-medium">{formatCurrency(product.details.annual_fee)}</p>
                        </div>
                        <div>
                            <p className="text-muted-foreground">Credit Limit</p>
                            <p className="font-medium">{formatCurrency(product.details.credit_limit)}</p>
                        </div>
                        <div>
                            <p className="text-muted-foreground">Rewards Rate</p>
                            <p className="font-medium">{product.details.rewards_rate}%</p>
                        </div>
                    </div>
                )
            case "Insurance":
                return (
                    <div className="grid grid-cols-2 gap-2 text-sm mt-2">
                        <div>
                            <p className="text-muted-foreground">Monthly Premium</p>
                            <p className="font-medium">{formatCurrency(product.details.monthly_premium)}</p>
                        </div>
                        <div>
                            <p className="text-muted-foreground">Deductible</p>
                            <p className="font-medium">{formatCurrency(product.details.deductible)}</p>
                        </div>
                        <div>
                            <p className="text-muted-foreground">Coverage Amount</p>
                            <p className="font-medium">{formatCurrency(product.details.coverage_amount)}</p>
                        </div>
                    </div>
                )
            case "Loan":
                return (
                    <div className="grid grid-cols-2 gap-2 text-sm mt-2">
                        <div>
                            <p className="text-muted-foreground">Interest Rate</p>
                            <p className="font-medium">{product.details.interest_rate}%</p>
                        </div>
                        <div>
                            <p className="text-muted-foreground">Loan Amount</p>
                            <p className="font-medium">{formatCurrency(product.details.loan_amount)}</p>
                        </div>
                        <div>
                            <p className="text-muted-foreground">Term</p>
                            <p className="font-medium">{product.details.term_months} months</p>
                        </div>
                    </div>
                )
            case "Investment":
                return (
                    <div className="grid grid-cols-2 gap-2 text-sm mt-2">
                        <div>
                            <p className="text-muted-foreground">Min Investment</p>
                            <p className="font-medium">{formatCurrency(product.details.min_investment)}</p>
                        </div>
                        <div>
                            <p className="text-muted-foreground">Expected Return</p>
                            <p className="font-medium">{product.details.expected_annual_return}%</p>
                        </div>
                        <div>
                            <p className="text-muted-foreground">Volatility</p>
                            <p className="font-medium">{product.details.volatility}/10</p>
                        </div>
                    </div>
                )
            default:
                return null
        }
    }

    // Get category icon
    const getCategoryIcon = (category: string) => {
        switch (category) {
            case "Credit Card":
                return <DollarSign className="h-5 w-5" />
            case "Insurance":
                return <ShieldCheck className="h-5 w-5" />
            case "Loan":
                return <AlertCircle className="h-5 w-5" />
            case "Investment":
                return <TrendingUp className="h-5 w-5" />
            default:
                return <Star className="h-5 w-5" />
        }
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>Product Recommendations</CardTitle>
                <CardDescription>Personalized financial product recommendations based on customer profile</CardDescription>
            </CardHeader>
            <CardContent>
                {topProducts && (
                    <div className="space-y-6">
                        {recommendations.map((recommendation, index: number) => (
                            <div key={index} className="border rounded-lg p-4">
                                <div className="flex items-start gap-2 mb-3">
                                    <div className="bg-primary/10 p-2 rounded-full">
                                        <Star className="h-5 w-5 text-primary" />
                                    </div>
                                    <div>
                                        <h3 className="font-medium">{recommendation.name}</h3>
                                        {/* <p className="text-sm text-muted-foreground">{recommendation.reason}</p> */}
                                    </div>
                                </div>

                                <Accordion type="single" collapsible className="w-full">
                                    {recommendation.products.map((product) => {
                                        return (
                                            <AccordionItem value={product.product_id} key={product.product_id}>
                                                <AccordionTrigger className="hover:no-underline">
                                                    <div className="flex items-center gap-2 text-left">
                                                        <div className="bg-muted p-1.5 rounded">{getCategoryIcon(product.category)}</div>
                                                        <div>
                                                            <div className="font-medium">{product.name}</div>
                                                            <div className="flex items-center gap-1 mt-1">
                                                                <Badge variant="outline" className="text-xs">
                                                                    {product.category}
                                                                </Badge>
                                                                <Badge variant="outline" className="text-xs">
                                                                    {product.subcategory}
                                                                </Badge>
                                                                <Badge className={`text-xs ${getTierColor(product.tier)}`}>{product.tier}</Badge>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </AccordionTrigger>
                                                <AccordionContent>
                                                    <div className="pl-9">
                                                        <p className="text-sm mb-2">{product.description}</p>

                                                        {renderProductDetails(product)}

                                                        <div className="grid grid-cols-3 gap-2 mt-4 text-xs">
                                                            <div className="flex flex-col items-center p-2 bg-muted rounded">
                                                                <span className="text-muted-foreground">Value</span>
                                                                <span className="font-medium">{product.value_customer}/10</span>
                                                            </div>
                                                            <div className="flex flex-col items-center p-2 bg-muted rounded">
                                                                <span className="text-muted-foreground">Risk</span>
                                                                <span className="font-medium">{product.risk_customer}/10</span>
                                                            </div>
                                                            <div className="flex flex-col items-center p-2 bg-muted rounded">
                                                                <span className="text-muted-foreground">Retention</span>
                                                                <span className="font-medium">{product.retention_value}/10</span>
                                                            </div>
                                                        </div>

                                                        {/* <Button className="w-full mt-4" size="sm">
                                                            Learn More
                                                        </Button> */}
                                                    </div>
                                                </AccordionContent>
                                            </AccordionItem>
                                        )
                                    })}
                                </Accordion>
                            </div>
                        ))}
                    </div>
                )}
            </CardContent>
        </Card>
    )
}

