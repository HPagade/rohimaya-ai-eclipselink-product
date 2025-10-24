import { redirect } from 'next/navigation';

export default function HomePage() {
  // Redirect to login page (will be handled by auth middleware later)
  redirect('/login');
}
