import NewListingDialog from "./new-listing-dialog";

export default function JobsPage() {
  return (
    <div className="page-transition p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Jobs</h1>
        <NewListingDialog />
      </div>
      <div>
        {/* Job listings will go here */}
      </div>
    </div>
  );
}
