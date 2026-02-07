declare module 'next-intl/server' {
  export type GetRequestConfigParams = {
    locale: string;
  };

  export type RequestConfig = {
    messages: Record<string, unknown>;
  };

  export function getRequestConfig(
    fn: (params: GetRequestConfigParams) => RequestConfig | Promise<RequestConfig>
  ): (params: GetRequestConfigParams) => Promise<RequestConfig>;
}
