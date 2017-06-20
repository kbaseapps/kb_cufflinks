package kb_cufflinks::kb_cufflinksClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
use Time::HiRes;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

kb_cufflinks::kb_cufflinksClient

=head1 DESCRIPTION


A KBase module: kb_cufflinks


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => kb_cufflinks::kb_cufflinksClient::RpcClient->new,
	url => $url,
	headers => [],
    };
    my %arg_hash = @args;
    $self->{async_job_check_time} = 0.1;
    if (exists $arg_hash{"async_job_check_time_ms"}) {
        $self->{async_job_check_time} = $arg_hash{"async_job_check_time_ms"} / 1000.0;
    }
    $self->{async_job_check_time_scale_percent} = 150;
    if (exists $arg_hash{"async_job_check_time_scale_percent"}) {
        $self->{async_job_check_time_scale_percent} = $arg_hash{"async_job_check_time_scale_percent"};
    }
    $self->{async_job_check_max_time} = 300;  # 5 minutes
    if (exists $arg_hash{"async_job_check_max_time_ms"}) {
        $self->{async_job_check_max_time} = $arg_hash{"async_job_check_max_time_ms"} / 1000.0;
    }
    my $service_version = undef;
    if (exists $arg_hash{"service_version"}) {
        $service_version = $arg_hash{"service_version"};
    }
    $self->{service_version} = $service_version;

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}

sub _check_job {
    my($self, @args) = @_;
# Authentication: ${method.authentication}
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function _check_job (received $n, expecting 1)");
    }
    {
        my($job_id) = @args;
        my @_bad_arguments;
        (!ref($job_id)) or push(@_bad_arguments, "Invalid type for argument 0 \"job_id\" (it should be a string)");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to _check_job:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => '_check_job');
        }
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cufflinks._check_job",
        params => \@args});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => '_check_job',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method _check_job",
                        status_line => $self->{client}->status_line,
                        method_name => '_check_job');
    }
}




=head2 CufflinksCall

  $return = $obj->CufflinksCall($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_cufflinks.CufflinksParams
$return is a kb_cufflinks.ResultsToReport
CufflinksParams is a reference to a hash where the following keys are defined:
	ws_id has a value which is a string
	sample_alignment has a value which is a string
	num_threads has a value which is an int
	min-intron-length has a value which is an int
	max-intron-length has a value which is an int
	overhang-tolerance has a value which is an int
ResultsToReport is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_cufflinks.CufflinksParams
$return is a kb_cufflinks.ResultsToReport
CufflinksParams is a reference to a hash where the following keys are defined:
	ws_id has a value which is a string
	sample_alignment has a value which is a string
	num_threads has a value which is an int
	min-intron-length has a value which is an int
	max-intron-length has a value which is an int
	overhang-tolerance has a value which is an int
ResultsToReport is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

sub CufflinksCall
{
    my($self, @args) = @_;
    my $job_id = $self->_CufflinksCall_submit(@args);
    my $async_job_check_time = $self->{async_job_check_time};
    while (1) {
        Time::HiRes::sleep($async_job_check_time);
        $async_job_check_time *= $self->{async_job_check_time_scale_percent} / 100.0;
        if ($async_job_check_time > $self->{async_job_check_max_time}) {
            $async_job_check_time = $self->{async_job_check_max_time};
        }
        my $job_state_ref = $self->_check_job($job_id);
        if ($job_state_ref->{"finished"} != 0) {
            if (!exists $job_state_ref->{"result"}) {
                $job_state_ref->{"result"} = [];
            }
            return wantarray ? @{$job_state_ref->{"result"}} : $job_state_ref->{"result"}->[0];
        }
    }
}

sub _CufflinksCall_submit {
    my($self, @args) = @_;
# Authentication: required
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function _CufflinksCall_submit (received $n, expecting 1)");
    }
    {
        my($params) = @args;
        my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to _CufflinksCall_submit:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => '_CufflinksCall_submit');
        }
    }
    my $context = undef;
    if ($self->{service_version}) {
        $context = {'service_ver' => $self->{service_version}};
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cufflinks._CufflinksCall_submit",
        params => \@args, context => $context});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => '_CufflinksCall_submit',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
            );
        } else {
            return $result->result->[0];  # job_id
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method _CufflinksCall_submit",
                        status_line => $self->{client}->status_line,
                        method_name => '_CufflinksCall_submit');
    }
}

 


=head2 run_Cuffdiff

  $return = $obj->run_Cuffdiff($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_cufflinks.CuffdiffParams
$return is a kb_cufflinks.RNASeqDifferentialExpression
CuffdiffParams is a reference to a hash where the following keys are defined:
	ws_id has a value which is a string
	rnaseq_exp_details has a value which is a kb_cufflinks.RNASeqSampleSet
	output_obj_name has a value which is a string
	time-series has a value which is a string
	library-type has a value which is a string
	library-norm-method has a value which is a string
	multi-read-correct has a value which is a string
	min-alignment-count has a value which is an int
	dispersion-method has a value which is a string
	no-js-tests has a value which is a string
	frag-len-mean has a value which is an int
	frag-len-std-dev has a value which is an int
	max-mle-iterations has a value which is an int
	compatible-hits-norm has a value which is a string
	no-length-correction has a value which is a string
RNASeqSampleSet is a reference to a hash where the following keys are defined:
	sampleset_id has a value which is a string
	sampleset_desc has a value which is a string
	domain has a value which is a string
	platform has a value which is a string
	num_samples has a value which is an int
	num_replicates has a value which is an int
	sample_ids has a value which is a reference to a list where each element is a string
	condition has a value which is a reference to a list where each element is a string
	source has a value which is a string
	Library_type has a value which is a string
	publication_Id has a value which is a string
	external_source_date has a value which is a string
RNASeqDifferentialExpression is a reference to a hash where the following keys are defined:
	tool_used has a value which is a string
	tool_version has a value which is a string
	tool_opts has a value which is a reference to a list where each element is a reference to a hash where the key is a string and the value is a string
	file has a value which is a kb_cufflinks.Handle
	sample_ids has a value which is a reference to a list where each element is a string
	condition has a value which is a reference to a list where each element is a string
	genome_id has a value which is a string
	expressionSet_id has a value which is a kb_cufflinks.ws_expressionSet_id
	alignmentSet_id has a value which is a kb_cufflinks.ws_alignmentSet_id
	sampleset_id has a value which is a kb_cufflinks.ws_Sampleset_id
	comments has a value which is a string
Handle is a reference to a hash where the following keys are defined:
	hid has a value which is a kb_cufflinks.HandleId
	file_name has a value which is a string
	id has a value which is a string
	type has a value which is a string
	url has a value which is a string
	remote_md5 has a value which is a string
	remote_sha1 has a value which is a string
HandleId is a string
ws_expressionSet_id is a string
ws_alignmentSet_id is a string
ws_Sampleset_id is a string

</pre>

=end html

=begin text

$params is a kb_cufflinks.CuffdiffParams
$return is a kb_cufflinks.RNASeqDifferentialExpression
CuffdiffParams is a reference to a hash where the following keys are defined:
	ws_id has a value which is a string
	rnaseq_exp_details has a value which is a kb_cufflinks.RNASeqSampleSet
	output_obj_name has a value which is a string
	time-series has a value which is a string
	library-type has a value which is a string
	library-norm-method has a value which is a string
	multi-read-correct has a value which is a string
	min-alignment-count has a value which is an int
	dispersion-method has a value which is a string
	no-js-tests has a value which is a string
	frag-len-mean has a value which is an int
	frag-len-std-dev has a value which is an int
	max-mle-iterations has a value which is an int
	compatible-hits-norm has a value which is a string
	no-length-correction has a value which is a string
RNASeqSampleSet is a reference to a hash where the following keys are defined:
	sampleset_id has a value which is a string
	sampleset_desc has a value which is a string
	domain has a value which is a string
	platform has a value which is a string
	num_samples has a value which is an int
	num_replicates has a value which is an int
	sample_ids has a value which is a reference to a list where each element is a string
	condition has a value which is a reference to a list where each element is a string
	source has a value which is a string
	Library_type has a value which is a string
	publication_Id has a value which is a string
	external_source_date has a value which is a string
RNASeqDifferentialExpression is a reference to a hash where the following keys are defined:
	tool_used has a value which is a string
	tool_version has a value which is a string
	tool_opts has a value which is a reference to a list where each element is a reference to a hash where the key is a string and the value is a string
	file has a value which is a kb_cufflinks.Handle
	sample_ids has a value which is a reference to a list where each element is a string
	condition has a value which is a reference to a list where each element is a string
	genome_id has a value which is a string
	expressionSet_id has a value which is a kb_cufflinks.ws_expressionSet_id
	alignmentSet_id has a value which is a kb_cufflinks.ws_alignmentSet_id
	sampleset_id has a value which is a kb_cufflinks.ws_Sampleset_id
	comments has a value which is a string
Handle is a reference to a hash where the following keys are defined:
	hid has a value which is a kb_cufflinks.HandleId
	file_name has a value which is a string
	id has a value which is a string
	type has a value which is a string
	url has a value which is a string
	remote_md5 has a value which is a string
	remote_sha1 has a value which is a string
HandleId is a string
ws_expressionSet_id is a string
ws_alignmentSet_id is a string
ws_Sampleset_id is a string


=end text

=item Description



=back

=cut

sub run_Cuffdiff
{
    my($self, @args) = @_;
    my $job_id = $self->_run_Cuffdiff_submit(@args);
    my $async_job_check_time = $self->{async_job_check_time};
    while (1) {
        Time::HiRes::sleep($async_job_check_time);
        $async_job_check_time *= $self->{async_job_check_time_scale_percent} / 100.0;
        if ($async_job_check_time > $self->{async_job_check_max_time}) {
            $async_job_check_time = $self->{async_job_check_max_time};
        }
        my $job_state_ref = $self->_check_job($job_id);
        if ($job_state_ref->{"finished"} != 0) {
            if (!exists $job_state_ref->{"result"}) {
                $job_state_ref->{"result"} = [];
            }
            return wantarray ? @{$job_state_ref->{"result"}} : $job_state_ref->{"result"}->[0];
        }
    }
}

sub _run_Cuffdiff_submit {
    my($self, @args) = @_;
# Authentication: required
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function _run_Cuffdiff_submit (received $n, expecting 1)");
    }
    {
        my($params) = @args;
        my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to _run_Cuffdiff_submit:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => '_run_Cuffdiff_submit');
        }
    }
    my $context = undef;
    if ($self->{service_version}) {
        $context = {'service_ver' => $self->{service_version}};
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cufflinks._run_Cuffdiff_submit",
        params => \@args, context => $context});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => '_run_Cuffdiff_submit',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
            );
        } else {
            return $result->result->[0];  # job_id
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method _run_Cuffdiff_submit",
                        status_line => $self->{client}->status_line,
                        method_name => '_run_Cuffdiff_submit');
    }
}

 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "kb_cufflinks.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cufflinks.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'run_Cuffdiff',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method run_Cuffdiff",
            status_line => $self->{client}->status_line,
            method_name => 'run_Cuffdiff',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for kb_cufflinks::kb_cufflinksClient\n";
    }
    if ($sMajor == 0) {
        warn "kb_cufflinks::kb_cufflinksClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 boolean

=over 4



=item Description

A boolean - 0 for false, 1 for true.
@range (0, 1)


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 ResultsToReport

=over 4



=item Description

Object for Report type


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 CufflinksParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ws_id has a value which is a string
sample_alignment has a value which is a string
num_threads has a value which is an int
min-intron-length has a value which is an int
max-intron-length has a value which is an int
overhang-tolerance has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ws_id has a value which is a string
sample_alignment has a value which is a string
num_threads has a value which is an int
min-intron-length has a value which is an int
max-intron-length has a value which is an int
overhang-tolerance has a value which is an int


=end text

=back



=head2 HandleId

=over 4



=item Description

Input parameters and output for run_cuffdiff


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 ws_Sampleset_id

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 ws_alignmentSet_id

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 ws_expressionSet_id

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 Handle

=over 4



=item Description

@optional hid file_name type url remote_md5 remote_sha1


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
hid has a value which is a kb_cufflinks.HandleId
file_name has a value which is a string
id has a value which is a string
type has a value which is a string
url has a value which is a string
remote_md5 has a value which is a string
remote_sha1 has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
hid has a value which is a kb_cufflinks.HandleId
file_name has a value which is a string
id has a value which is a string
type has a value which is a string
url has a value which is a string
remote_md5 has a value which is a string
remote_sha1 has a value which is a string


=end text

=back



=head2 RNASeqSampleSet

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
sampleset_id has a value which is a string
sampleset_desc has a value which is a string
domain has a value which is a string
platform has a value which is a string
num_samples has a value which is an int
num_replicates has a value which is an int
sample_ids has a value which is a reference to a list where each element is a string
condition has a value which is a reference to a list where each element is a string
source has a value which is a string
Library_type has a value which is a string
publication_Id has a value which is a string
external_source_date has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
sampleset_id has a value which is a string
sampleset_desc has a value which is a string
domain has a value which is a string
platform has a value which is a string
num_samples has a value which is an int
num_replicates has a value which is an int
sample_ids has a value which is a reference to a list where each element is a string
condition has a value which is a reference to a list where each element is a string
source has a value which is a string
Library_type has a value which is a string
publication_Id has a value which is a string
external_source_date has a value which is a string


=end text

=back



=head2 CuffdiffParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ws_id has a value which is a string
rnaseq_exp_details has a value which is a kb_cufflinks.RNASeqSampleSet
output_obj_name has a value which is a string
time-series has a value which is a string
library-type has a value which is a string
library-norm-method has a value which is a string
multi-read-correct has a value which is a string
min-alignment-count has a value which is an int
dispersion-method has a value which is a string
no-js-tests has a value which is a string
frag-len-mean has a value which is an int
frag-len-std-dev has a value which is an int
max-mle-iterations has a value which is an int
compatible-hits-norm has a value which is a string
no-length-correction has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ws_id has a value which is a string
rnaseq_exp_details has a value which is a kb_cufflinks.RNASeqSampleSet
output_obj_name has a value which is a string
time-series has a value which is a string
library-type has a value which is a string
library-norm-method has a value which is a string
multi-read-correct has a value which is a string
min-alignment-count has a value which is an int
dispersion-method has a value which is a string
no-js-tests has a value which is a string
frag-len-mean has a value which is an int
frag-len-std-dev has a value which is an int
max-mle-iterations has a value which is an int
compatible-hits-norm has a value which is a string
no-length-correction has a value which is a string


=end text

=back



=head2 RNASeqDifferentialExpression

=over 4



=item Description

Result of run_CuffDiff
Object RNASeqDifferentialExpression file structure
@optional tool_opts tool_version sample_ids comments


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
tool_used has a value which is a string
tool_version has a value which is a string
tool_opts has a value which is a reference to a list where each element is a reference to a hash where the key is a string and the value is a string
file has a value which is a kb_cufflinks.Handle
sample_ids has a value which is a reference to a list where each element is a string
condition has a value which is a reference to a list where each element is a string
genome_id has a value which is a string
expressionSet_id has a value which is a kb_cufflinks.ws_expressionSet_id
alignmentSet_id has a value which is a kb_cufflinks.ws_alignmentSet_id
sampleset_id has a value which is a kb_cufflinks.ws_Sampleset_id
comments has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
tool_used has a value which is a string
tool_version has a value which is a string
tool_opts has a value which is a reference to a list where each element is a reference to a hash where the key is a string and the value is a string
file has a value which is a kb_cufflinks.Handle
sample_ids has a value which is a reference to a list where each element is a string
condition has a value which is a reference to a list where each element is a string
genome_id has a value which is a string
expressionSet_id has a value which is a kb_cufflinks.ws_expressionSet_id
alignmentSet_id has a value which is a kb_cufflinks.ws_alignmentSet_id
sampleset_id has a value which is a kb_cufflinks.ws_Sampleset_id
comments has a value which is a string


=end text

=back



=cut

package kb_cufflinks::kb_cufflinksClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
