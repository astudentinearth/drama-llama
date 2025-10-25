import type { AxiosResponse } from "axios";

export function success(response: AxiosResponse) {
  return response.status >= 200 && response.status < 300;
}
