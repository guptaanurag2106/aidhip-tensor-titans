/* eslint-disable @typescript-eslint/no-explicit-any */
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { z } from "zod";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error("Missing `VITE_API_BASE_URL` env variable.");
}

const convertStringArrayToArray = (s: string) =>
  s.split(",").map((v) => v.trim());

// Define schemas
const CustomerInfoSchema = z.object({
  age: z.number(),
  balance: z.array(z.number()), // check
  credit_score: z.number(),
  customer_id: z.string(),
  education: z.string(),
  gender: z.string(),
  goals: z.array(z.string()), // check
  income: z.number(),
  is_married: z.boolean(),
  job: z.string(),
  loan_amts: z.array(z.number()), // check
  location: z.string(),
  main_purchase_cat: z.array(z.string()), // check
  monthly_spending: z.array(z.number()), // check
  num_of_children: z.number(),
  preferred_payment_method: z.string(),
  satisfaction: z.number(),
  support_interaction_count: z.number(),
  input_params: z.string(),
  output_params: z.string(),
  top_n_products: z.array(z.string()),
  top_n_passive_products: z.array(z.string()),
});

const CustomerSupportHistorySchema = z.object({
  complaint_id: z.string(),
  customer_id: z.string(),
  date: z.string(),
  is_repeating_issue: z.boolean(),
  main_concerns: z.array(z.string()),
  sentiment: z.number(),
  transcript: z.string(),
  was_issue_resolved: z.boolean(),
});

const CustomerPurchaseHistorySchema = z.object({
  amt: z.number(),
  customer_id: z.string(),
  date: z.string(),
  item_brand: z.string(),
  item_category: z.string(),
  item_sub_category: z.string(),
  location: z.string(),
  payment_method: z.string(),
  platform: z.string(),
  transaction_id: z.string(),
});

const CustomerSocialMediaHistorySchema = z.object({
  brands_liked: z.array(z.string()),
  customer_id: z.string(),
  date: z.string(),
  engagement_level: z.number(),
  feedback_on_financial_products: z.string(),
  image_url: z.string(),
  platform: z.string(),
  post_id: z.string(),
  sentiment_score: z.number(),
  text_content: z.string(),
  topics_of_interest: z.array(z.string()),
});

export type CustomerInfo = z.infer<typeof CustomerInfoSchema>;
export type CustomerSupportHistory = z.infer<
  typeof CustomerSupportHistorySchema
>;

export const useCustomerIds = () => {
  return useQuery({
    queryKey: ["customer-ids"],
    queryFn: async () => {
      const response = await axios.get(`${API_BASE_URL}/customer_ids`);
      return response.data as string[];
    },
  });
};

const convertStringToArraysForCustomerInfo = (customerInfo: any) => ({
  ...customerInfo,
  balance: customerInfo.balance
    ? convertStringArrayToArray(customerInfo.balance).map((v: string) =>
        parseFloat(v)
      )
    : [],
  goals: customerInfo.goals
    ? convertStringArrayToArray(customerInfo.goals)
    : [],
  loan_amts: customerInfo.loan_amts
    ? convertStringArrayToArray(customerInfo.loan_amts).map((v: string) =>
        parseFloat(v)
      )
    : [],
  main_purchase_cat: customerInfo.main_purchase_cat
    ? convertStringArrayToArray(customerInfo.main_purchase_cat)
    : [],
  monthly_spending: customerInfo.monthly_spending
    ? convertStringArrayToArray(customerInfo.monthly_spending).map(
        (v: string) => parseFloat(v)
      )
    : [],
  top_n_products: customerInfo.top_n_products
    ? convertStringArrayToArray(customerInfo.top_n_products)
    : [],
  top_n_passive_products: customerInfo.top_n_passive_products
    ? convertStringArrayToArray(customerInfo.top_n_passive_products)
    : [],
});

const convertStringToArraysForSupportRecord = (supportRecord: any) => ({
  ...supportRecord,
  main_concerns: convertStringArrayToArray(supportRecord.main_concerns) ?? [],
});

const convertStringToArraysForSocialMediaRecord = (socialMedia: any) => ({
  ...socialMedia,
  brands_liked: socialMedia.brands_liked
    ? convertStringArrayToArray(socialMedia.brands_liked)
    : [],
  topics_of_interest: socialMedia.topics_of_interest
    ? convertStringArrayToArray(socialMedia.topics_of_interest)
    : [],
});

// Fetch customer info
export const useCustomerInfo = (customerId: string) => {
  return useQuery({
    queryKey: ["customer-info", customerId],
    queryFn: async () => {
      const response = await axios.get(`${API_BASE_URL}/customer_profile`, {
        params: { customer_id: customerId },
      });
      if (response?.data?.error) {
        return { error: response.data.error } as { error: string };
      }
      try {
        return CustomerInfoSchema.parse(
          convertStringToArraysForCustomerInfo(response.data)
        );
      } catch (err) {
        console.log(err);
      }
    },
    enabled: !!customerId,
  });
};

export const updateCustomerInfo = async ({
  customerId,
  data,
}: {
  customerId: string;
  data: CustomerInfo;
}): Promise<{ customer_id: string }> => {
  return axios
    .post(`${API_BASE_URL}/customer-info`, data, {
      params: { customer_id: customerId },
    })
    .then((res) => res.data);
};

// Update customer info
export const useUpdateCustomerInfo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateCustomerInfo,
    onSuccess: ({ customer_id }: { customer_id: string }) => {
      queryClient.invalidateQueries({
        queryKey: ["customer-info", customer_id],
      });
    },
  });
};

// Fetch customer support history
export const useCustomerSupportHistory = (customerId: string) => {
  return useQuery({
    queryKey: ["customer-support-history", customerId],
    queryFn: async () => {
      const response = await axios.get(
        `${API_BASE_URL}/customer_support_history`,
        {
          params: { customer_id: customerId },
        }
      );
      if (response?.data?.error) {
        return { error: response.data.error } as { error: string };
      }
      return z
        .array(CustomerSupportHistorySchema)
        .parse(response.data.map(convertStringToArraysForSupportRecord));
    },
    enabled: !!customerId,
  });
};

export const addCustomerSupportHistory = async ({
  customerId,
  data,
}: {
  customerId: string;
  data: any;
}): Promise<{ customer_id: string }> => {
  return axios
    .post(`${API_BASE_URL}/customer_support_history`, data, {
      params: { customer_id: customerId },
    })
    .then((res) => res.data);
};

export const useAddCustomerSupportHistory = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: addCustomerSupportHistory,
    onSuccess: ({ customer_id }: { customer_id: string }) => {
      queryClient.invalidateQueries({
        queryKey: ["customer-support-history", customer_id],
      });
    },
  });
};

export const useCustomerPurchaseHistory = (customerId: string) => {
  return useQuery({
    queryKey: ["customer-purchase-history", customerId],
    queryFn: async () => {
      const response = await axios.get(
        `${API_BASE_URL}/customer_purchase_history`,
        {
          params: { customer_id: customerId },
        }
      );
      if (response?.data?.error) {
        return { error: response.data.error } as { error: string };
      }
      return z.array(CustomerPurchaseHistorySchema).parse(response.data);
    },
    enabled: !!customerId,
  });
};

export const addCustomerPurchaseHistory = async ({
  customerId,
  data,
}: {
  customerId: string;
  data: any;
}): Promise<{ customer_id: string }> => {
  return axios
    .post(`${API_BASE_URL}/customer_purchase_history`, data, {
      params: { customer_id: customerId },
    })
    .then((res) => res.data);
};

export const useAddCustomerPurchaseHistory = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: addCustomerPurchaseHistory,
    onSuccess: ({ customer_id }: { customer_id: string }) => {
      queryClient.invalidateQueries({
        queryKey: ["customer-purchase-history", customer_id],
      });
    },
  });
};

export const useCustomerSocialMediaHistory = (customerId: string) => {
  return useQuery({
    queryKey: ["customer-social-media-history", customerId],
    queryFn: async () => {
      const response = await axios.get(
        `${API_BASE_URL}/customer_social_media_history`,
        {
          params: { customer_id: customerId },
        }
      );
      if (response?.data?.error) {
        return { error: response.data.error } as { error: string };
      }
      try {
        return z
          .array(CustomerSocialMediaHistorySchema)
          .parse(response.data.map(convertStringToArraysForSocialMediaRecord));
      } catch (err) {
        console.log(err);
      }
    },
    enabled: !!customerId,
  });
};

export const addCustomerSocialMediaHistory = async ({
  customerId,
  data,
}: {
  customerId: string;
  data: any;
}): Promise<{ customer_id: string }> => {
  return axios
    .post(`${API_BASE_URL}/customer_social_media_history`, data, {
      params: { customer_id: customerId },
    })
    .then((res) => res.data);
};

export const useAddCustomerSocialMediaHistory = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: addCustomerSocialMediaHistory,
    onSuccess: ({ customer_id }: { customer_id: string }) => {
      queryClient.invalidateQueries({
        queryKey: ["customer-social-media-history", customer_id],
      });
    },
  });
};

export const customerRunAi = async ({
  customerId,
}: {
  customerId: string;
}): Promise<{ customer_id: string }> => {
  return axios
    .post(`${API_BASE_URL}/customer_run_ai`, {
      params: { customer_id: customerId },
    })
    .then((res) => res.data);
};

export const useCustomerRunAi = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: customerRunAi,
    onSuccess: ({ customer_id }: { customer_id: string }) => {
      queryClient.invalidateQueries({
        queryKey: ["customer-info", customer_id],
      });
    },
  });
};