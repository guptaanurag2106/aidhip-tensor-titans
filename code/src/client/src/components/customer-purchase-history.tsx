import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useAddCustomerPurchaseHistory, useCustomerPurchaseHistory } from "@/lib/api"
import { formatDate } from "@/lib/utils"

// Categories for form
const CATEGORIES = ["Electronics", "Clothing", "Home", "Books", "Beauty", "Sports", "Groceries"]
const PLATFORMS = ["Online", "In-store", "Mobile App"]
const PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Cash", "Bank Transfer"]

interface CustomerPurchaseHistoryProps {
  customerId: string
}

export default function CustomerPurchaseHistory({ customerId }: CustomerPurchaseHistoryProps) {
  const { data: purchases, isLoading } = useCustomerPurchaseHistory(customerId);
  const { mutateAsync } = useAddCustomerPurchaseHistory()
  const [showForm, setShowForm] = useState(false)

  // Form state
  const [category, setCategory] = useState<string>("")
  const [subCategory, setSubCategory] = useState<string>("")
  const [brand, setBrand] = useState<string>("")
  const [price, setPrice] = useState<string>("")
  const [platform, setPlatform] = useState<string>("")
  const [paymentMethod, setPaymentMethod] = useState<string>("")
  const [location, setLocation] = useState<string>("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const lastTxnId = purchases && !("error" in purchases)
      ? parseInt(purchases[purchases.length - 1].transaction_id.split("_")[1])
      : 0

    // Create new purchase record
    const newPurchase = {
      transaction_id: `TXN_${lastTxnId + 1}`,
      item_category: category,
      item_sub_category: subCategory,
      item_brand: brand,
      amt: Number.parseFloat(price),
      date: new Date().toLocaleDateString("en-GB"),
      platform,
      payment_method: paymentMethod,
    }

    // Reset form
    setCategory("")
    setSubCategory("")
    setBrand("")
    setPrice("")
    setPlatform("")
    setPaymentMethod("")
    setLocation("")
    setShowForm(false)

    console.log("New purchase added:", newPurchase);
    mutateAsync({
      customerId,
      data: newPurchase
    })
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Purchase History</CardTitle>
        <CardDescription>View and manage customer purchase records</CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <p className="text-center py-4">Loading purchase history...</p>
        ) : purchases && "error" in purchases ?
          (
            <p className="text-center py-4">{purchases.error}</p>
          ) : purchases ?
            (
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
                  {purchases?.map((purchase) => (
                    <TableRow key={purchase.transaction_id}>
                      <TableCell>{formatDate(purchase.date)}</TableCell>
                      <TableCell>{purchase.item_category}</TableCell>
                      <TableCell>{purchase.item_sub_category}</TableCell>
                      <TableCell>{purchase.item_brand}</TableCell>
                      <TableCell className="text-right">${purchase.amt.toFixed(2)}</TableCell>
                      <TableCell>{purchase.platform}</TableCell>
                      <TableCell>{purchase.payment_method}</TableCell>
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
                <Label htmlFor="location">Location</Label>
                <Input id="location" value={location} onChange={(e) => setLocation(e.target.value)} required />
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
        {!showForm && (
          <Button onClick={() => setShowForm(true)}>
            Add New Purchase Record
          </Button>
        )}
      </CardFooter>
    </Card>
  )
}

