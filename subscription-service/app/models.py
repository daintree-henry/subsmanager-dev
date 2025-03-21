from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app import db


class SubscriptionProvider(db.Model):
    __tablename__ = 'subscription_providers'

    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(100), nullable=False, unique=True)
    business_registration_number = db.Column(db.String(20))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(20))
    status = db.Column(
        db.String(20),
        default='active',
        nullable=False,
        info={'choices': ['active', 'inactive', 'suspended']}
    )
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    subscription_plans = relationship('SubscriptionPlan', back_populates='provider')

    def __repr__(self):
        return f'<SubscriptionProvider {self.id}: {self.provider_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'provider_name': self.provider_name,
            'business_registration_number': self.business_registration_number,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plans'

    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('subscription_providers.id'), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)
    monthly_fee = db.Column(db.Numeric(10, 2), nullable=False)
    billing_cycle_months = db.Column(db.Integer, default=1)
    features = db.Column(JSONB)
    is_active = db.Column(db.Boolean, default=True)
    logo_file_name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    provider = relationship('SubscriptionProvider', back_populates='subscription_plans')
    user_subscriptions = relationship('UserSubscription', back_populates='subscription_plan')

    __table_args__ = (
        db.UniqueConstraint('provider_id', 'plan_name', name='uq_provider_plan_name'),
    )

    def __repr__(self):
        return f'<SubscriptionPlan {self.id}: {self.plan_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'provider_id': self.provider_id,
            'plan_name': self.plan_name,
            'monthly_fee': float(self.monthly_fee),
            'billing_cycle_months': self.billing_cycle_months,
            'features': self.features,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subscription_plan_id = db.Column(
        db.Integer,
        db.ForeignKey('subscription_plans.id'),
        nullable=False
    )
    start_date = db.Column(db.Date, nullable=False)
    next_billing_date = db.Column(db.Date, nullable=False)
    auto_renewal = db.Column(db.Boolean, default=True)
    payment_method = db.Column(db.String(50))
    status = db.Column(
        db.String(20),
        default='active',
        nullable=False,
        info={'choices': ['active', 'cancelled', 'suspended', 'expired']}
    )
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    subscription_plan = relationship('SubscriptionPlan', back_populates='user_subscriptions')
    payments = relationship('SubscriptionPayment', back_populates='subscription')

    def __repr__(self):
        return f'<UserSubscription {self.id}: Plan {self.subscription_plan_id} - {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subscription_plan_id': self.subscription_plan_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'next_billing_date': self.next_billing_date.isoformat() if self.next_billing_date else None,
            'auto_renewal': self.auto_renewal,
            'payment_method': self.payment_method,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class SubscriptionPayment(db.Model):
    __tablename__ = 'subscription_payments'

    id = db.Column(db.Integer, primary_key=True)
    user_subscription_id = db.Column(
        db.Integer,
        db.ForeignKey('user_subscriptions.id'),
        nullable=False
    )
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    payment_status = db.Column(
        db.String(20),
        default='pending',
        nullable=False,
        info={'choices': ['successful', 'failed', 'pending', 'refunded']}
    )
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    # Relationships
    subscription = relationship('UserSubscription', back_populates='payments')

    def __repr__(self):
        return f'<SubscriptionPayment {self.id}: {self.amount_paid} - {self.payment_status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_subscription_id': self.user_subscription_id,
            'amount_paid': float(self.amount_paid),
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


