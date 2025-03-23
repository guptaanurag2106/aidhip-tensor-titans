/* eslint-disable @typescript-eslint/no-explicit-any */
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { z } from "zod";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error("Missing `VITE_API_BASE_URL` env variable.");
}

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
  balance: customerInfo.balance?.split(",").map((v: string) => parseFloat(v)) ?? [],
  goals: customerInfo.goals?.split(",") ?? [],
  loan_amts: customerInfo.loan_amts?.split(",").map((v: string) => parseFloat(v)) ?? [],
  main_purchase_cat: customerInfo.main_purchase_cat?.split(",") ?? [],
  monthly_spending:
    customerInfo.monthly_spending?.split(",").map((v: string) => parseFloat(v)) ?? [],
});

const convertStringToArraysForSupportRecord = (supportRecord: any) => ({
  ...supportRecord,
  main_concerns: supportRecord.main_concerns?.split(",") ?? [],
})

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
      return CustomerInfoSchema.parse(
        convertStringToArraysForCustomerInfo(response.data)
      );
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
}): Promise<{ customerId: string }> => {
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
    onSuccess: ({ customerId }: { customerId: string }) => {
      queryClient.invalidateQueries({
        queryKey: ["customer-info", customerId],
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
      console.log(response.data.map(convertStringToArraysForSupportRecord))
      return z.array(CustomerSupportHistorySchema).parse(response.data.map(convertStringToArraysForSupportRecord));
    },
    enabled: !!customerId,
  });
};

export const addCustomerSupportHistory = async ({
  customerId,
  data,
}: {
  customerId: string;
  data: CustomerSupportHistory;
}): Promise<{ customerId: string }> => {
  return axios
    .post(`${API_BASE_URL}/customer-support-history`, data, {
      params: { customer_id: customerId },
    })
    .then((res) => res.data);
};

export const useAddCustomerSupportHistory = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: addCustomerSupportHistory,
    onSuccess: ({ customerId }: { customerId: string }) => {
      queryClient.invalidateQueries({
        queryKey: ["customer-support-history", customerId],
      });
    },
  });
};
