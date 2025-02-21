import uuid
import hashlib

from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.contrib.auth.models import User
from django.db.models import JSONField
from reportlab.lib.pagesizes import elevenSeventeen

from grout.models import GroutModel, Record, RecordType
from django.contrib.postgres.fields import ArrayField
from django.db import connections

FILE_UPLOAD_STATUS = (
    ('PENDING', 'PENDING'),
    ('COMPLETED', 'COMPLETED'),
    ('ERROR', 'ERROR')
)

UPLOADED_FROM = (
    ('Web', 'Web'),
    ('iOS', 'iOS'),
    ('Android', 'Android'),
    ('bulk_upload', 'bulk_upload')
)
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class DriverRecord(Record):
    """Extend Grout Record model with custom fields"""
    weather = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    light = models.CharField(max_length=50, null=True, blank=True, db_index=True)

    city = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    city_district = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    neighborhood = models.CharField(max_length=50, null=True, blank=True)
    road = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    merged_and_updated = models.BooleanField(default=False)
    merged_uuid = models.CharField(max_length=500, null=True, blank=True)
    uploaded_from = models.CharField(choices=UPLOADED_FROM, max_length=15, default='Web')
    identity = models.CharField(max_length=50, unique=True, editable=False, null=True)

    def generate_incident_identity_value(self, auto_increment_id):
        """
        Use:- to generate value for identity of the incident.
        Example: 0225FDAYHOI101-1
        02 - Last two digits of the month
        25 - Last two digits of the year
        Severity Initials (F = Fatal, S = Serious, M = Minor)
        First three letters of Light - Day, Daw, Dus, Nig
        Main Cause Initials (D = Driver Error, HOI = Hit Object In Road, HOO = Hit Object Off Road)
        Collision Type Initials , for eg (HO = Head On, V = Vehicle Defect, R = Road Defect, O = Other)
        Crash Type Number - 101
        Auto-incremental ID - 1
        """
        # Extract required fields from payload with defaults
        month = str(self.occurred_from)[5:7]  # Last two digits of month
        year = str(self.occurred_from)[2:4]  # Last two digits of year
        light = "000" if str(self.light) == "" else str(self.light)[:3].upper() # First three letters of light or '000'

        severity = self.data['driverIncidentDetails'].get('Severity', '0')[0].upper()  # Severity initial or '0'

        # Main Cause Initials
        main_cause = self.data['driverIncidentDetails'].get('Main Cause', '0')
        main_cause_initials = '0' if main_cause == '0' else "D" if main_cause == "Driver Error" else "V" if main_cause == "Vehicle defect" else "R" if (
                main_cause == "Road defect") else "O"
        # main_cause_initials = 'D'.join([word[0].upper() for word in main_cause.split()]) if main_cause != '0' else '0'

        # Collision Type Initials
        collision_type = self.data['driverIncidentDetails'].get('Collision Type', '0')
        # collision_type_initials = ''.join(
        #     [word[0].upper() for word in collision_type.split()]) if collision_type != '0' else '0'
        collision_type_initials = '0' if collision_type == '0' else "HO" if collision_type == "Head on" else "RE" if collision_type == "Rear End" else "RA" if collision_type == "Right angle" else "A" if collision_type == "Angle (Other)" else "SS" if collision_type == "Side swipe" else "OV" if collision_type == "Overturned vehicle" else "HOI" if collision_type == "Hit object in road" else "HOO" if collision_type == "Hit object off road" else "HPV" if collision_type == "Hit parked vehicle" else "HP" if collision_type == "Hit pedestrian" else "HA" if collision_type == "Hit animal" else "OTH"

        # Crash Type Number from Movement Code
        crash_type_number = self.data['driverCrashDiagram'].get('Movement Code', '0').split(' – ')[
            0]  # Extract number part

        # Final Identity String
        identity = f"{month}{year}{severity}{light}{main_cause_initials}{collision_type_initials}{crash_type_number}-{auto_increment_id}"
        return identity

    def generate_intervention_identity_value(self, auto_increment_id):
        """
        Use:- to generate value for identity of the incident.
        Example: 0225FDAYHOI101-1
        02 - Last two digits of the month
        25 - Last two digits of the year
        Severity Initials (F = Fatal, S = Serious, M = Minor)
        First three letters of Light - Day, Daw, Dus, Nig
        Main Cause Initials (D = Driver Error, HOI = Hit Object In Road, HOO = Hit Object Off Road)
        Collision Type Initials , for eg (HO = Head On, V = Vehicle Defect, R = Road Defect, O = Other)
        Crash Type Number - 101
        Auto-incremental ID - 1
        """
        # Extract required fields from payload with defaults
        month = str(self.occurred_from)[5:7]  # Last two digits of month
        year = str(self.occurred_from)[2:4]  # Last two digits of year

        # Final Identity String
        identity = f"{month}{year}{0}{000}{0}{000}-{auto_increment_id}"
        return identity

    def save(self, *args, **kwargs):
        auto_increment_id = self.identity.split('-')[-1] if self.identity else None

        if not self.identity:
            with connections['default'].cursor() as cursor:
                # pg sequence used for thread safety
                cursor.execute("SELECT nextval('record_identity_seq')")
                auto_increment_id = cursor.fetchone()[0]

        # Generate identity based on payload and existing sequence number
        if "driverIncidentDetails" in self.data.keys():
           generated_identity = self.generate_incident_identity_value(auto_increment_id)
           logger.info('---incident identity--{}---'.format(generated_identity))
        # elif "driverInterventionDetails" in self.data.keys():
        else:
           generated_identity = self.generate_intervention_identity_value(auto_increment_id)
           logger.info('----identity--{}---'.format(generated_identity.strip()))
        self.identity = generated_identity

        return super(Record, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #   """
    #   Extend the model's save method to run custom field validators.
    #   """
    #   auto_increment_id = self.identity.split('-')[-1] if self.identity else None
    #
    #   if not self.identity:
    #     with connections['default'].cursor() as cursor:
    #       # pg sequence used for threadsafety
    #       cursor.execute("SELECT nextval('record_identity_seq')")
    #       next_number = cursor.fetchone()[0]
    #     self.identity = f"MWTI-{next_number:07d}"
    #
    #   return super(Record, self).save(*args, **kwargs)


class RecordAuditLogEntry(models.Model):
    """Records an occurrence of a Record being altered, who did it, and when.

    Note that 'user' and 'record' are maintained as foreign keys for convenience querying,
    but these fields can be set to NULL if the referenced object is deleted. If a user or
    record has been deleted, then 'username' or 'record_uuid' should be used, respectively.
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Store both a foreign key and the username so that if the user is deleted this can still
    # be useful.
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=100, db_index=True)
    # Same for the record; if the record this refers to is deleted we still want to be able to
    # determine which audit log entries pertained to that record.
    record = models.ForeignKey(DriverRecord, null=True, on_delete=models.SET_NULL)
    record_uuid = models.CharField(max_length=100, db_index=True)

    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class ActionTypes(object):
        CREATE = 'create'
        UPDATE = 'update'
        DELETE = 'delete'

        choices = (
            (CREATE, 'Create'),
            (UPDATE, 'Update'),
            (DELETE, 'Delete')
        )

        @classmethod
        def as_list(cls):
            return [cls.CREATE, cls.UPDATE, cls.DELETE]

    action = models.CharField(max_length=50, choices=ActionTypes.choices)

    # The log JSON will contain `old` and `new` state of the model
    log = models.TextField(null=True)
    # Singature will contain an MD5 hash of the log field
    signature = models.CharField(max_length=100, null=True)

    def verify_log(self):
        if self.log is None:
            return True
        return hashlib.md5(self.log).hexdigest() == str(self.signature)


class DedupeJob(models.Model):
    """ Stores information about a celery job
    """

    class Status(object):
        """Status of job"""
        PENDING = 'PENDING'
        STARTED = 'STARTED'
        SUCCESS = 'SUCCESS'
        ERROR = 'ERROR'
        CHOICES = (
            (PENDING, 'Pending'),
            (STARTED, 'Started'),
            (SUCCESS, 'Success'),
            (ERROR, 'Error'),
        )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=8, choices=Status.CHOICES, default=Status.PENDING)
    celery_task = models.UUIDField(null=True)

    class Meta(object):
        get_latest_by = 'datetime'


class RecordDuplicate(GroutModel):
    """ Store information about a possible duplicate record pair
    Duplicates are found using a time-distance heuristic
    """
    record = models.ForeignKey(DriverRecord, null=True, related_name="record", on_delete=models.SET_NULL)

    duplicate_record = models.ForeignKey(DriverRecord, null=True,
                                         related_name="duplicate_record", on_delete=models.SET_NULL)
    score = models.FloatField(default=0)
    resolved = models.BooleanField(default=False)
    job = models.ForeignKey(DedupeJob, on_delete=models.CASCADE)
    potential_duplicates = ArrayField(models.TextField(null=True, blank=True), null=True, blank=True)


class RecordCostConfig(GroutModel):
    """Store a configuration for calculating costs of incidents.

    This takes the form of a reference to an enum field on a RecordType, along with user-
    configurable mapping of societal costs for each possible value of that enum.
    """
    #: The record type whose records should be cost-aggregated
    # This will likely need to be set automatically by the front-end
    record_type = models.ForeignKey(RecordType, on_delete=models.CASCADE)

    #: Key of the schema property to access (Related Content Type, e.g.'accidentDetails')
    # This will also likely need to be set automatically by the front-end, or at least filtered so
    # that users cannot select content types which allow multiple entries
    content_type_key = models.TextField()

    #: Key of the content type property to access (e.g. 'Severity')
    # This will need to be filadmin/tered on the front-end to enums.
    property_key = models.TextField()

    #: User-configurable prefix to cost values
    cost_prefix = models.CharField(max_length=6, blank=True, null=True)

    #: User-configurable suffix to cost values
    cost_suffix = models.CharField(max_length=6, blank=True, null=True)

    @property
    def path(self):
        """Gets the field path specified by this object within a schema"""
        return [self.content_type_key, 'properties', self.property_key]

    #: Mappings between enumerations and cost values (e.g. {'Fatal': 1000000,
    #                                                       'Serious injury': 50000, ...})
    # This should be auto-populated by the front-end once a property_key is selected.
    enum_costs = HStoreField()


class DriverRecordCopy(Record):
    """To keep history of records Extend Grout Record model with custom fields"""
    record = models.ForeignKey(DriverRecord, on_delete=models.CASCADE)
    weather = models.CharField(max_length=50, null=True, blank=True)
    light = models.CharField(max_length=50, null=True, blank=True)

    city = models.CharField(max_length=50, null=True, blank=True)
    city_district = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    neighborhood = models.CharField(max_length=50, null=True, blank=True)
    road = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    uploaded_from = models.CharField(choices=UPLOADED_FROM, max_length=15, default='Web')


# Save data for CrashDiagram
class CrashDiagramOrientation(GroutModel):
    """ Store information about a possible crashdiagram record  """
    crash_type = models.CharField(max_length=150, null=True, blank=True)

    movement_code = models.CharField(max_length=65, null=True, blank=True, unique=True, error_messages={
        'unique': ("A movement_code already exists."),
    })
    image = JSONField()
    is_active = models.BooleanField(default=True)


class WeatherInfo(models.Model):
    provider_name = models.CharField(max_length=100, null=True, blank=True)
    client_id = models.CharField(max_length=100, null=True)
    client_secret = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)


class IrapDetail(models.Model):
    irap_treatment_id = models.IntegerField(null=False, blank=False, default=1000, primary_key=False)
    irap_treatment_name = models.CharField(max_length=200, null=False, blank=False)
    irap_treatment_description = models.TextField(null=True, blank=True)
    path = models.URLField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)


class DuplicateDistanceConfig(models.Model):
    """Holds user-configurable settings for location in determining duplicates"""
    dedupe_distance_threshold = models.FloatField(default=0.0008)
    unit = models.CharField(max_length=10, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class BulkUploadDetail(models.Model):
    file_name = models.CharField(max_length=100, null=True, blank=True)
    file_status = models.CharField(max_length=30, choices=FILE_UPLOAD_STATUS, default='PENDING')
    csv_uploaded_date = models.DateTimeField(auto_now_add=True)
    record_type = models.CharField(max_length=30, null=True, blank=True)


class WeatherDataList(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.label


class KeyDetail(models.Model):
    keyname = models.CharField(max_length=50, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
