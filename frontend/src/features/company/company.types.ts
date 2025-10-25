export interface Company {
  id: string;
  name: string;
  description: string;
}

export interface UpdateCompanyDTO {
  name: string;
  description: string;
}