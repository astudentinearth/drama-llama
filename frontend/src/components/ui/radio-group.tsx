import * as React from "react"
import { cn } from "@/lib/utils"

interface RadioGroupContextType {
  value?: string;
  onValueChange?: (value: string) => void;
  name: string;
}

const RadioGroupContext = React.createContext<RadioGroupContextType | null>(null);

interface RadioGroupProps {
  value?: string;
  onValueChange?: (value: string) => void;
  className?: string;
  children: React.ReactNode;
}

interface RadioGroupItemProps {
  value: string;
  id?: string;
  className?: string;
}

const RadioGroup = React.forwardRef<HTMLDivElement, RadioGroupProps>(
  ({ className, value, onValueChange, children, ...props }, ref) => {
    const name = React.useId();
    
    return (
      <RadioGroupContext.Provider value={{ value, onValueChange, name }}>
        <div
          className={cn("grid gap-2", className)}
          ref={ref}
          role="radiogroup"
          {...props}
        >
          {children}
        </div>
      </RadioGroupContext.Provider>
    )
  }
)
RadioGroup.displayName = "RadioGroup"

const RadioGroupItem = React.forwardRef<HTMLInputElement, RadioGroupItemProps>(
  ({ className, value, id, ...props }, ref) => {
    const context = React.useContext(RadioGroupContext);
    
    if (!context) {
      throw new Error("RadioGroupItem must be used within a RadioGroup");
    }
    
    const { value: groupValue, onValueChange, name } = context;
    const isChecked = groupValue === value;
    
    return (
      <input
        type="radio"
        ref={ref}
        id={id}
        name={name}
        value={value}
        checked={isChecked}
        onChange={() => onValueChange?.(value)}
        className={cn(
          "aspect-square h-4 w-4 rounded-full border-2 border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 cursor-pointer",
          isChecked && "bg-primary border-primary",
          className
        )}
        {...props}
      />
    )
  }
)
RadioGroupItem.displayName = "RadioGroupItem"

export { RadioGroup, RadioGroupItem }