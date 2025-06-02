use REST::Client;
use JSON;
# Data::Dumper makes it easy to see what the JSON returned actually looks like 
# when converted into Perl data structures.
use Data::Dumper;
use MIME::Base64;

sub toList {
   my $data = shift;
   my $key = shift;
   if (ref($data->{$key}) eq 'ARRAY') {
       $data->{$key};
   } elsif (ref($data->{$key}) eq 'HASH') {
       [$data->{$key}];
   } else {
       [];
   }
}
if ($#ARGV ne 0) {
    print "usage: $0 <username>\n";
    exit 1;
}
my $reviewerToRemove = $ARGV[0];
my $username = 'admin';
my $password = 'admin';
my $headers = {Accept => 'application/json', Authorization => 'Basic ' . encode_base64($username . ':' . $password)};
my $client = REST::Client->new();
$client->setHost('http://localhost:3990');
$client->GET(
    '/fecru/rest-service/reviews-v1/filter/allOpenReviews', 
    $headers
);
my $response = from_json($client->responseContent());
my $reviews = toList($response->{'reviews'},'reviewData');
foreach $review (@$reviews) {
    my $id = $review->{'permaId'}->{'id'};
    $client->GET(
        '/fecru/rest-service/reviews-v1/' . $id . '/reviewers/uncompleted', 
        $headers
    );
    my $response = from_json($client->responseContent());
    my $incompleteReviewers = toList($response->{'reviewers'},'reviewer');
    foreach $reviewer (@$incompleteReviewers) {
        $myreviewerUserName = $reviewer->{'userName'};
        if ($reviewerToRemove eq $myreviewerUserName) {
            print "Removing " . $reviewer->{'displayName'} . " from review " . $id . "\n";
            $client->DELETE(
                '/fecru/rest-service/reviews-v1/' . $id . '/reviewers/' . $reviewer->{'userName'}, 
                $headers
            );
            print Dumper($client->responseContent());
        }
    }
}
