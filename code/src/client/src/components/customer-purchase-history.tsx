import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { format } from "date-fns"

// Mock purchase data
const MOCK_PURCHASES = {
  CUST001: [
    {
      id: "P001",
      category: "Electronics",
      subCategory: "Smartphones",
      brand: "Apple",
      price: 999,
      date: "2023-05-15",
      platform: "Online",
      paymentMethod: "Credit Card",
    },
    {
      id: "P002",
      category: "Clothing",
      subCategory: "Shirts",
      brand: "Nike",
      price: 49.99,
      date: "2023-06-22",
      platform: "In-store",
      paymentMethod: "Cash",
    },
  ],
  CUST002: [
    {
      id: "P003",
      category: "Home",
      subCategory: "Furniture",
      brand: "IKEA",
      price: 299,
      date: "2023-04-10",
      platform: "Online",
      paymentMethod: "PayPal",
    },
  ],
  CUST003: [
    {
      id: "P004",
      category: "Electronics",
      subCategory: "Laptops",
      brand: "Dell",
      price: 1299,
      date: "2023-07-05",
      platform: "Online",
      paymentMethod: "Credit Card",
    },
    {
      id: "P005",
      category: "Books",
      subCategory: "Fiction",
      brand: "Penguin",
      price: 19.99,
      date: "2023-07-12",
      platform: "Online",
      paymentMethod: "Debit Card",
    },
    {
      id: "P006",
      category: "Groceries",
      subCategory: "Snacks",
      brand: "Various",
      price: 45.5,
      date: "2023-07-18",
      platform: "In-store",
      paymentMethod: "Cash",
    },
  ],
  CUST004: [
    {
      id: "P007",
      category: "Beauty",
      subCategory: "Skincare",
      brand: "Cerave",
      price: 35.99,
      date: "2023-06-30",
      platform: "Online",
      paymentMethod: "Credit Card",
    },
  ],
  CUST005: [
    {
      id: "P008",
      category: "Sports",
      subCategory: "Equipment",
      brand: "Adidas",
      price: 129.99,
      date: "2023-05-28",
      platform: "In-store",
      paymentMethod: "Credit Card",
    },
    {
      id: "P009",
      category: "Electronics",
      subCategory: "Headphones",
      brand: "Sony",
      price: 199.99,
      date: "2023-06-15",
      platform: "Online",
      paymentMethod: "PayPal",
    },
  ],
}

// Categories for form
const CATEGORIES = ["Electronics", "Clothing", "Home", "Books", "Beauty", "Sports", "Groceries"]
const PLATFORMS = ["Online", "In-store", "Mobile App"]
const PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Cash", "Bank Transfer"]

interface CustomerPurchaseHistoryProps {
  customerId: string
}

export default function CustomerPurchaseHistory({ customerId }: CustomerPurchaseHistoryProps) {
  const [purchases, setPurchases] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)

  // Form state
  const [category, setCategory] = useState<string>("")
  const [subCategory, setSubCategory] = useState<string>("")
  const [brand, setBrand] = useState<string>("")
  const [price, setPrice] = useState<string>("")
  const [platform, setPlatform] = useState<string>("")
  const [paymentMethod, setPaymentMethod] = useState<string>("")

  // Simulate API fetch
  useEffect(() => {
    const fetchPurchases = async () => {
      // Simulate network delay
      await new Promise((resolve) => setTimeout(resolve, 300))
      setPurchases(MOCK_PURCHASES[customerId as keyof typeof MOCK_PURCHASES] || [])
      setLoading(false)
    }

    fetchPurchases()
  }, [customerId])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // Create new purchase record
    const newPurchase = {
      id: `P${Math.floor(Math.random() * 1000)}`,
      category,
      subCategory,
      brand,
      price: Number.parseFloat(price),
      date: new Date().toISOString().split("T")[0],
      platform,
      paymentMethod,
    }

    // Add to purchases
    setPurchases([...purchases, newPurchase])

    // Reset form
    setCategory("")
    setSubCategory("")
    setBrand("")
    setPrice("")
    setPlatform("")
    setPaymentMethod("")
    setShowForm(false)

    console.log("New purchase added:", newPurchase)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Purchase History</CardTitle>
        <CardDescription>View and manage customer purchase records</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <p className="text-center py-4">Loading purchase history...</p>
        ) : purchases.length > 0 ? (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Sub-Category</TableHead>
                <TableHead>Brand</TableHead>
                <TableHead className="text-right">Price</TableHead>
                <TableHead>Platform</TableHead>
                <TableHead>Payment</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {purchases.map((purchase) => (
                <TableRow key={purchase.id}>
                  <TableCell>{format(new Date(purchase.date), "MMM d, yyyy")}</TableCell>
                  <TableCell>{purchase.category}</TableCell>
                  <TableCell>{purchase.subCategory}</TableCell>
                  <TableCell>{purchase.brand}</TableCell>
                  <TableCell className="text-right">${purchase.price.toFixed(2)}</TableCell>
                  <TableCell>{purchase.platform}</TableCell>
                  <TableCell>{purchase.paymentMethod}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        ) : (
          <p className="text-center py-4">No purchase history found for this customer.</p>
        )}

        {showForm && (
          <form onSubmit={handleSubmit} className="mt-6 space-y-4 border rounded-lg p-4">
            <h3 className="text-lg font-medium">Add New Purchase</h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="category">Category</Label>
                <Select value={category} onValueChange={setCategory} required>
                  <SelectTrigger id="category">
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    {CATEGORIES.map((cat) => (
                      <SelectItem key={cat} value={cat}>
                        {cat}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="subCategory">Sub-Category</Label>
                <Input id="subCategory" value={subCategory} onChange={(e) => setSubCategory(e.target.value)} required />
              </div>

              <div className="space-y-2">
                <Label htmlFor="brand">Brand</Label>
                <Input id="brand" value={brand} onChange={(e) => setBrand(e.target.value)} required />
              </div>

              <div className="space-y-2">
                <Label htmlFor="price">Price ($)</Label>
                <Input
                  id="price"
                  type="number"
                  min="0.01"
                  step="0.01"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="platform">Platform</Label>
                <Select value={platform} onValueChange={setPlatform} required>
                  <SelectTrigger id="platform">
                    <SelectValue placeholder="Select platform" />
                  </SelectTrigger>
                  <SelectContent>
                    {PLATFORMS.map((plat) => (
                      <SelectItem key={plat} value={plat}>
                        {plat}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="paymentMethod">Payment Method</Label>
                <Select value={paymentMethod} onValueChange={setPaymentMethod} required>
                  <SelectTrigger id="paymentMethod">
                    <SelectValue placeholder="Select payment method" />
                  </SelectTrigger>
                  <SelectContent>
                    {PAYMENT_METHODS.map((method) => (
                      <SelectItem key={method} value={method}>
                        {method}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="flex justify-end space-x-2 pt-2">
              <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
              <Button type="submit">Add Purchase</Button>
            </div>
          </form>
        )}
      </CardContent>
      <CardFooter className="flex justify-between">
        <div>{!loading && <span className="text-sm text-muted-foreground">{purchases.length} records found</span>}</div>
        {!showForm && <Button onClick={() => setShowForm(true)}>Add New Purchase</Button>}
      </CardFooter>
    </Card>
  )
}

