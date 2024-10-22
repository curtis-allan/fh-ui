import { clsx, type ClassValue } from "https://esm.sh/clsx"
import { twMerge } from "https://esm.sh/tailwind-merge"

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
    }