"use client";

import type React from "react";

import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useAddCustomerSocialMediaHistory, useCustomerSocialMediaHistory } from "@/lib/api";
import { formatDate } from "@/lib/utils";

// Platform options
const PLATFORMS = ["Instagram", "Twitter", "Facebook", "TikTok", "LinkedIn"];

interface CustomerSocialMediaProps {
  customerId: string;
}

export default function CustomerSocialMedia({
  customerId,
}: CustomerSocialMediaProps) {
  const { data: socialMedia, isLoading } =
    useCustomerSocialMediaHistory(customerId);
  const { mutateAsync } = useAddCustomerSocialMediaHistory()
  const [showForm, setShowForm] = useState(false);

  // Form state
  const [text, setText] = useState<string>("");
  const [platform, setPlatform] = useState<string>("");
  const [topics, setTopics] = useState<string>("");
  const [influencersFollowed, setInfluencersFollowed] = useState<string>("");
  const [brandsLiked, setBrandsLiked] = useState<string>("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const lastPostId =
      socialMedia && !("error" in socialMedia)
        ? parseInt(socialMedia[socialMedia.length - 1].post_id.split("_")[1])
        : 0;

    // Create new social media record
    const newSocialMedia = {
      post_id: `POST_${lastPostId + 1}`,
      date: new Date().toLocaleDateString("en-GB"),
      platform,
      image_url: "",
      text_content: text,
      influencers_followed: influencersFollowed,
      topics_of_interest: topics,
      brands_liked: brandsLiked,
    };

    // Reset form
    setText("");
    setPlatform("");
    setTopics("");
    setBrandsLiked("");
    setInfluencersFollowed("");
    setShowForm(false);

    console.log("New social media record added:", newSocialMedia);
    mutateAsync({
      customerId,
      data: newSocialMedia
    })
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Social Media Activity</CardTitle>
        <CardDescription>
          View and manage customer social media interactions
        </CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <p className="text-center py-4">Loading social media activity...</p>
        ) : socialMedia && "error" in socialMedia ? (
          <p className="text-center py-4">{socialMedia.error}</p>
        ) : socialMedia ? (
          <div className="space-y-6">
            {socialMedia.map((social) => (
              <div key={social.post_id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center gap-2">
                    <div className="font-medium">{social.platform}</div>
                    <div className="text-sm text-muted-foreground">
                      {formatDate(social.date)}
                    </div>
                  </div>
                  <div
                    className={`px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-800`}
                  >
                    {social.sentiment_score}
                  </div>
                </div>

                <div className="mb-3">
                  <p>{social.text_content}</p>
                </div>

                {social.image_url &&
                  social.image_url.indexOf("example.com/") == -1 && (
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
                  {social.topics_of_interest.map(
                    (topic: string, index: number) => (
                      <span
                        key={index}
                        className="bg-muted px-2 py-1 rounded-full text-xs"
                      >
                        {topic}
                      </span>
                    )
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center py-4">
            No social media activity found for this customer.
          </p>
        )}

        {showForm && (
          <form
            onSubmit={handleSubmit}
            className="mt-6 space-y-4 border rounded-lg p-4"
          >
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

              <div className="space-y-2">
                <Label htmlFor="topics">
                  Topics of interest (comma separated)
                </Label>
                <Input
                  id="topics"
                  value={topics}
                  onChange={(e) => setTopics(e.target.value)}
                  placeholder="e.g. Technology, Fashion, Travel"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="influencersFollowed">
                  Influencers Followed
                </Label>
                <Input
                  id="influencersFollowed"
                  type="number"
                  min="0"
                  step="1"
                  value={influencersFollowed}
                  onChange={(e) => setInfluencersFollowed(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="brandsLiked">Brands Liked</Label>
                <Input
                  id="brandsLiked"
                  type="number"
                  min="0"
                  step="1"
                  value={brandsLiked}
                  onChange={(e) => setBrandsLiked(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="flex justify-end space-x-2 pt-2">
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowForm(false)}
              >
                Cancel
              </Button>
              <Button type="submit">Add Social Media Record</Button>
            </div>
          </form>
        )}
      </CardContent>
      <CardFooter className="flex justify-between">
        {!showForm && (
          <Button onClick={() => setShowForm(true)}>
            Add New Social Record
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}
