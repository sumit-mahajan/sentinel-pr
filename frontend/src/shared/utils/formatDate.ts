import { format } from 'date-fns';

export function formatDate(value: string) {
  return format(new Date(value), 'MMM d, yyyy HH:mm');
}
