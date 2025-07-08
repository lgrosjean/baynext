// components/newsletter-form.tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@workspace/ui/components/button";
import { Input } from "@workspace/ui/components/input";
import { MailIcon } from "lucide-react";
import { toast } from "sonner";

const schema = z.object({
  email: z.string().email(),
});

type FormData = z.infer<typeof schema>;

export default function NewsletterForm() {
  
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isValidating },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    
      try {
        const res = await fetch("/api/subscribe", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: data.email }),
        });

        if (res.ok) {
          reset();
          toast.success("Thank you for subscribing!");
        } else {
          const json = await res.json();
          toast.error(json.error || "Something went wrong.");
        }
      } catch {
        toast.error("Subscription failed. Please try again later.");
      }
    };
  

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col md:flex-row items-center justify-center gap-4 max-w-lg mx-auto">
      <Input
        type="email"
        placeholder="Your email"
        {...register("email")}
        className="w-full md:w-auto"
      />
      <Button type="submit" className="flex items-center gap-2" disabled={isValidating}>
        <MailIcon className="w-4 h-4" />
        {isValidating ? "Subscribing..." : "Subscribe"}
      </Button>
      {errors.email && (
        <p className="w-full text-center mt-2 text-sm text-red-400">{errors.email.message}</p>
      )}
    </form>
  );
}
