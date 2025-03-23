"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { format } from "date-fns"

// Mock social media data
const MOCK_SOCIAL = {
  CUST001: [
    {
      id: "SM001",
      date: "2023-07-05",
      hasImage: true,
      text: "Just got my new smartphone! The camera quality is amazing! #NewPhone #Photography",
      platform: "Instagram",
      sentiment: "Positive",
      topics: ["Technology", "Photography"],
    },
    {
      id: "SM002",
      date: "2023-07-12",
      hasImage: false,
      text: "Having issues with my recent purchase. The battery life is not as advertised. @CompanySupport",
      platform: "Twitter",
      sentiment: "Negative",
      topics: ["Customer Service", "Product Issues"],
    },
  ],
  CUST002: [
    {
      id: "SM003",
      date: "2023-06-28",
      hasImage: true,
      text: "My new furniture setup is complete! Thanks for the quality products. #HomeDecor",
      platform: "Instagram",
      sentiment: "Positive",
      topics: ["Home Decor", "Lifestyle"],
    },
  ],
  CUST003: [
    {
      id: "SM004",
      date: "2023-07-10",
      hasImage: false,
      text: "Just finished this amazing book! Highly recommend to all sci-fi fans. #BookReview",
      platform: "Facebook",
      sentiment: "Positive",
      topics: ["Books", "Entertainment"],
    },
  ],
  CUST004: [
    {
      id: "SM005",
      date: "2023-07-02",
      hasImage: true,
      text: "My skincare routine with these new products. Seeing great results! #SkinCare #BeautyRoutine",
      platform: "Instagram",
      sentiment: "Positive",
      topics: ["Beauty", "Lifestyle"],
    },
  ],
  CUST005: [
    {
      id: "SM006",
      date: "2023-06-25",
      hasImage: true,
      text: "New workout gear! Ready to hit the gym. #Fitness #ActiveLifestyle",
      platform: "Instagram",
      sentiment: "Positive",
      topics: ["Fitness", "Lifestyle"],
    },
    {
      id: "SM007",
      date: "2023-07-08",
      hasImage: false,
      text: "These headphones have amazing sound quality! Perfect for my daily commute. #MusicLover",
      platform: "Twitter",
      sentiment: "Positive",
      topics: ["Music", "Technology"],
    },
  ],
}

// Platform options
const PLATFORMS = ["Instagram", "Twitter", "Facebook", "TikTok", "LinkedIn"]
const SENTIMENTS = ["Positive", "Neutral", "Negative"]

interface CustomerSocialMediaProps {
  customerId: string
}

export default function CustomerSocialMedia({ customerId }: CustomerSocialMediaProps) {
  const [socialMedia, setSocialMedia] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)

  // Form state
  const [text, setText] = useState<string>("")
  const [hasImage, setHasImage] = useState<boolean>(false)
  const [platform, setPlatform] = useState<string>("")
  const [sentiment, setSentiment] = useState<string>("")
  const [topics, setTopics] = useState<string>("")

  // Simulate API fetch
  useEffect(() => {
    const fetchSocialMedia = async () => {
      // Simulate network delay
      await new Promise((resolve) => setTimeout(resolve, 300))
      setSocialMedia(MOCK_SOCIAL[customerId as keyof typeof MOCK_SOCIAL] || [])
      setLoading(false)
    }

    fetchSocialMedia()
  }, [customerId])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // Create new social media record
    const newSocialMedia = {
      id: `SM${Math.floor(Math.random() * 1000)}`,
      date: new Date().toISOString().split("T")[0],
      hasImage,
      text,
      platform,
      sentiment,
      topics: topics.split(",").map((topic) => topic.trim()),
    }

    // Add to social media
    setSocialMedia([...socialMedia, newSocialMedia])

    // Reset form
    setText("")
    setHasImage(false)
    setPlatform("")
    setSentiment("")
    setTopics("")
    setShowForm(false)

    console.log("New social media record added:", newSocialMedia)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Social Media Activity</CardTitle>
        <CardDescription>View and manage customer social media interactions</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <p className="text-center py-4">Loading social media activity...</p>
        ) : socialMedia.length > 0 ? (
          <div className="space-y-6">
            {socialMedia.map((social) => (
              <div key={social.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center gap-2">
                    <div className="font-medium">{social.platform}</div>
                    <div className="text-sm text-muted-foreground">{format(new Date(social.date), "MMM d, yyyy")}</div>
                  </div>
                  <div
                    className={`px-2 py-1 rounded-full text-xs ${social.sentiment === "Positive"
                        ? "bg-green-100 text-green-800"
                        : social.sentiment === "Negative"
                          ? "bg-red-100 text-red-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                  >
                    {social.sentiment}
                  </div>
                </div>

                <div className="mb-3">
                  <p>{social.text}</p>
                </div>

                {social.hasImage && (
                  <div className="mb-3">
                    <img
                      src="/placeholder.svg?height=300&width=400"
                      alt="Social media post"
                      width={400}
                      height={300}
                      className="rounded-md object-cover"
                    />
                  </div>
                )}

                <div className="flex flex-wrap gap-1">
                  {social.topics.map((topic: string, index: number) => (
                    <span key={index} className="bg-muted px-2 py-1 rounded-full text-xs">
                      {topic}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center py-4">No social media activity found for this customer.</p>
        )}

        {showForm && (
          <form onSubmit={handleSubmit} className="mt-6 space-y-4 border rounded-lg p-4">
            <h3 className="text-lg font-medium">Add New Social Media Record</h3>

            <div className="space-y-4">
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
                <Label htmlFor="text">Post Text</Label>
                <Textarea
                  id="text"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Enter post content"
                  rows={3}
                  required
                />
              </div>

              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="hasImage"
                  checked={hasImage}
                  onChange={(e) => setHasImage(e.target.checked)}
                  className="rounded border-gray-300 text-primary focus:ring-primary"
                />
                <Label htmlFor="hasImage">Has Image</Label>
              </div>

              <div className="space-y-2">
                <Label htmlFor="sentiment">Sentiment</Label>
                <Select value={sentiment} onValueChange={setSentiment} required>
                  <SelectTrigger id="sentiment">
                    <SelectValue placeholder="Select sentiment" />
                  </SelectTrigger>
                  <SelectContent>
                    {SENTIMENTS.map((sent) => (
                      <SelectItem key={sent} value={sent}>
                        {sent}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="topics">Topics (comma separated)</Label>
                <Input
                  id="topics"
                  value={topics}
                  onChange={(e) => setTopics(e.target.value)}
                  placeholder="e.g. Technology, Fashion, Travel"
                  required
                />
              </div>
            </div>

            <div className="flex justify-end space-x-2 pt-2">
              <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
              <Button type="submit">Add Social Media Record</Button>
            </div>
          </form>
        )}
      </CardContent>
      <CardFooter className="flex justify-between">
        <div>
          {!loading && <span className="text-sm text-muted-foreground">{socialMedia.length} records found</span>}
        </div>
        {!showForm && <Button onClick={() => setShowForm(true)}>Add New Social Media Record</Button>}
      </CardFooter>
    </Card>
  )
}

